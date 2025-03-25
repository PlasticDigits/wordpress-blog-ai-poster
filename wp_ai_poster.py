#!/usr/bin/env python3
"""
WordPress AI Blog Post Generator

This script uses OpenAI to generate blog posts and uploads them to WordPress.
"""

import os
import argparse
import json
import time
import re
import random
import base64
from datetime import datetime
import requests
from dotenv import load_dotenv
from openai import OpenAI
import sys
import traceback
import copy

# Import custom modules
from blog_topic import get_random_topic
from blog_style import analyze_and_enhance
import wp_add_meta  # Import the new metadata module

# Version information
VERSION = "2.0.0"  # Major update with outline-based generation

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# WordPress Configuration
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

# Default blog post settings
DEFAULT_CATEGORY_ID = os.getenv("DEFAULT_CATEGORY_ID")
if DEFAULT_CATEGORY_ID and DEFAULT_CATEGORY_ID.strip().isdigit():
    DEFAULT_CATEGORY_ID = int(DEFAULT_CATEGORY_ID)
DEFAULT_CATEGORY_NAME = os.getenv("DEFAULT_CATEGORY_NAME", "Uncategorized").split('#')[0].strip()
DEFAULT_TAGS = os.getenv("DEFAULT_TAGS", "ai,generated,content").split('#')[0].strip().split(",")
DEFAULT_STATUS = os.getenv("DEFAULT_STATUS", "draft").split('#')[0].strip()

# Path to context and style markdown files
CONTEXT_STYLE_FILE = os.getenv("CONTEXT_STYLE_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "Context_Style.md"))
CONTEXT_KNOWLEDGE_FILE = os.getenv("CONTEXT_KNOWLEDGE_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "Context_Knowledge.md"))
CONTEXT_GOAL_FILE = os.getenv("CONTEXT_GOAL_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "Context_Goal.md"))

def setup_argparse():
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate and post AI content to WordPress")
    
    # Content generation options
    parser.add_argument("--topic", help="Topic for the blog post (if not provided, a random topic will be generated)")
    parser.add_argument("--length", type=int, default=None, 
                        help="Target word count for the blog post (default: random 2000-2500)")
    parser.add_argument("--context", action="append", 
                        help="Additional context for the blog post. Can be used multiple times.")
    parser.add_argument("--temperature", type=float, default=0.7, 
                        help="Temperature for AI generation (0.0-1.0, default: 0.7)")
    parser.add_argument("--no-research", action="store_true", 
                        help="Disable web research (research is enabled by default)")
    parser.add_argument("--loop", type=int, default=1,
                        help="Number of times to run the script (default: 1)")
                        
    # WordPress posting options
    parser.add_argument("--skip-post", action="store_true", 
                        help="Skip posting to WordPress, just generate content")
    parser.add_argument("--category-name", default=None, 
                        help=f"WordPress category name (default: {DEFAULT_CATEGORY_NAME})")
    parser.add_argument("--category-id", type=int, default=DEFAULT_CATEGORY_ID,
                        help="WordPress category ID (bypasses category name lookup)")
    parser.add_argument("--tags", default=None, 
                        help=f"Comma-separated list of tags (default: {','.join(DEFAULT_TAGS)})")
    parser.add_argument("--status", default=DEFAULT_STATUS, 
                        choices=["draft", "publish", "pending", "private"], 
                        help=f"Post status (default: {DEFAULT_STATUS})")
    parser.add_argument("--keyphrases", type=int, default=5, 
                        help="Number of keyphrases to generate (default: 5)")
                        
    # WordPress authentication options
    parser.add_argument("--auth-method", choices=["basic", "jwt", "application"], 
                        help="Authentication method to use with WordPress")
    parser.add_argument("--use-application-password", action="store_true", 
                        help="Use WordPress Application Password for authentication")
                        
    # File handling options
    parser.add_argument("--load-file", help="Load existing content from file instead of generating")
    parser.add_argument("--output-file", help="Save generated content to file")
    parser.add_argument("--skip-meta", action="store_true",
                        help="Skip generating meta description and keyphrases")
                        
    # Miscellaneous options
    parser.add_argument("--debug", action="store_true", 
                        help="Enable debug output")
    parser.add_argument("--version", action="store_true", 
                        help="Show version information")
    
    return parser.parse_args()

def connect_to_openai():
    """Initialize OpenAI client."""
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not found. Please set it in your .env file.")
    
    return OpenAI(api_key=OPENAI_API_KEY)

def get_wordpress_headers(auth_method=None, use_application_password=False):
    """Create authentication headers for WordPress REST API."""
    if not all([WP_URL, WP_USERNAME, WP_PASSWORD]):
        raise ValueError("WordPress credentials not found. Please set them in your .env file.")
    
    # Log authentication attempt
    print(f"Authenticating to WordPress REST API at {WP_URL}")
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Determine which authentication method to use
    if auth_method == "application" or use_application_password:
        print("Using Application Passwords authentication method")
        # Application Passwords format
        credentials = f"{WP_USERNAME}:{WP_PASSWORD}"
        token = base64.b64encode(credentials.encode())
        headers['Authorization'] = f'Basic {token.decode("utf-8")}'
    elif auth_method == "jwt":
        print("Using JWT authentication method")
        # Try to get a JWT token
        try:
            token_url = f"{WP_URL.rstrip('/')}/wp-json/jwt-auth/v1/token"
            token_data = {
                'username': WP_USERNAME,
                'password': WP_PASSWORD
            }
            token_response = requests.post(token_url, json=token_data)
            if token_response.status_code == 200:
                token_info = token_response.json()
                headers['Authorization'] = f'Bearer {token_info["token"]}'
                print("JWT authentication successful")
            else:
                print(f"JWT authentication failed: {token_response.status_code}")
                print("Falling back to Basic authentication")
                # Fall back to basic auth
                credentials = f"{WP_USERNAME}:{WP_PASSWORD}"
                token = base64.b64encode(credentials.encode())
                headers['Authorization'] = f'Basic {token.decode("utf-8")}'
        except Exception as e:
            print(f"JWT authentication attempt failed: {e}")
            print("Falling back to Basic authentication")
            # Fall back to basic auth
            credentials = f"{WP_USERNAME}:{WP_PASSWORD}"
            token = base64.b64encode(credentials.encode())
            headers['Authorization'] = f'Basic {token.decode("utf-8")}'
    else:
        print("Using Basic authentication method")
        # Standard Basic Auth
        credentials = f"{WP_USERNAME}:{WP_PASSWORD}"
        token = base64.b64encode(credentials.encode())
        headers['Authorization'] = f'Basic {token.decode("utf-8")}'
    
    # Test the authentication method
    test_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/users/me"
    try:
        print("Testing authentication...")
        response = requests.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("Authentication successful!")
            return headers
        
        # If unauthorized, show message but continue (the header might work for posting)
        if response.status_code in [401, 403]:
            print(f"Authentication test returned {response.status_code}. This might indicate:")
            print("- Your credentials are not correct")
            print("- The site requires Application Passwords (use --use-application-password)")
            print("- The REST API requires different authentication (try --auth-method)")
            print("Continuing anyway, but you might encounter errors when posting.")
            
            # Try a public endpoint to check if the API is functional
            print("Checking if REST API is accessible...")
            try:
                public_url = f"{WP_URL.rstrip('/')}/wp-json"
                public_response = requests.get(public_url, timeout=10)
                if public_response.status_code == 200:
                    print("REST API is accessible. This confirms the issue is with authentication.")
                else:
                    print(f"REST API check failed with status {public_response.status_code}.")
                    print("The WordPress site might not have REST API enabled.")
            except Exception as e:
                print(f"REST API check failed: {e}")
                print("This could indicate the WordPress site is not accessible.")
        else:
            print(f"Authentication test returned unexpected status code: {response.status_code}")
            
        # We'll return the headers anyway and let the actual post operation handle any auth issues
        return headers
    except Exception as e:
        print(f"Authentication test failed: {e}")
        print("Continuing with generated headers, but posting might fail.")
        return headers

def read_markdown_file(file_path):
    """Read content from a markdown file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        return ""
    except Exception as e:
        print(f"Error reading markdown file: {e}")
        return ""

def extract_content_sections(markdown_text):
    """Extract sections from markdown content."""
    sections = {}
    
    # Try to identify headers and their content
    header_pattern = r'^#+\s+(.*?)\s*$'
    headers = re.finditer(header_pattern, markdown_text, re.MULTILINE)
    
    last_pos = 0
    current_header = "Introduction"
    
    for match in headers:
        header = match.group(1)
        start_pos = match.start()
        
        # Get content of previous section
        if last_pos > 0:
            section_content = markdown_text[last_pos:start_pos].strip()
            sections[current_header] = section_content
        
        current_header = header
        last_pos = match.end()
    
    # Last section
    if last_pos > 0:
        sections[current_header] = markdown_text[last_pos:].strip()
    elif not sections:
        # If no headers found, use all content
        sections["Content"] = markdown_text
    
    return sections

def create_blog_prompt(args):
    """Create a detailed prompt for the AI to generate an outline based on user arguments, context, and style."""
    # Get current date for context
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Read content from markdown files
    context_style_content = read_markdown_file(CONTEXT_STYLE_FILE)
    context_knowledge_content = read_markdown_file(CONTEXT_KNOWLEDGE_FILE)
    context_goal_content = read_markdown_file(CONTEXT_GOAL_FILE)
    
    # Extract sections from markdown files for style and knowledge
    style_sections = extract_content_sections(context_style_content)
    knowledge_sections = extract_content_sections(context_knowledge_content)
    
    # Compile all knowledge sections
    all_knowledge_content = ""
    for section_title, section_content in knowledge_sections.items():
        if section_title != "Introduction":  # Skip the introduction section if it exists
            all_knowledge_content += f"\n## {section_title}\n{section_content}\n"
    
    if not all_knowledge_content:
        all_knowledge_content = "Assume the reader has basic familiarity with the topic but would benefit from deeper insights."
        
    # Compile all style sections
    all_style_content = ""
    for section_title, section_content in style_sections.items():
        if section_title != "Introduction":  # Skip the introduction section if it exists
            all_style_content += f"\n## {section_title}\n{section_content}\n"
    
    if not all_style_content:
        all_style_content = "Professional but conversational tone with engaging and persuasive writing."
    
    # Start with outline generation prompt
    prompt = f"""

    [GOALS]
    {context_goal_content}
    
    [KNOWLEDGE]
    {context_knowledge_content}
    
    [STYLE]
    {context_style_content}

    [INSTRUCTIONS]
    Create a detailed outline for a blog post about {args.topic}.
    Only write the outline, no other text - do not inlude lines like --- or markdown.

    On the first line, write the title of the blog post.
    For each section title, start with "##" and then the section title.
    For each section description, start with a * and then the section description.

    Today's date is {current_date}.
    Write to accomplish [GOALS].
    Use [KNOWLEDGE] to inform your writing.
    Write in the style of [STYLE].
    """
    
    return prompt

def generate_section_prompt(title, section_title, section_description, outline, current_date, total_words, num_sections):
    """Create a prompt to generate a specific section of the blog post."""
    # Estimate appropriate section length based on total word count and number of sections
    # Allow roughly 15% for intro and 15% for conclusion, the rest divided among main sections

    # Handle case when total_words is None by using a default value
    if total_words is None:
        # Use a reasonable default word count (can adjust as needed)
        total_words = random.randint(2000, 2500)
        print(f"Warning: No word count provided. Using default of {total_words} words.")

    approx_section_words = int((total_words) / max(1, num_sections))
    
    # Read the style guide directly
    try:
        with open("Context_Style.md", "r", encoding="utf-8") as f:
            style_guide_content = f.read()
    except Exception as e:
        print(f"Warning: Could not read style guide file: {e}")
        style_guide_content = "Persuasive style"
    
    # Read the goal content directly
    try:
        with open("Context_Goal.md", "r", encoding="utf-8") as f:
            goal_content = f.read()
    except Exception as e:
        print(f"Warning: Could not read goal file: {e}")
        goal_content = "Convince the reader you are correct"
    
    # Read the knowledge content directly
    try:
        with open("Context_Knowledge.md", "r", encoding="utf-8") as f:
            context_knowledge_content = f.read()
    except Exception as e:
        print(f"Warning: Could not read knowledge file: {e}")
        context_knowledge_content = "You have no special knowledge."
    
    prompt = f"""
    [GOALS]
    {goal_content}
    
    [KNOWLEDGE]
    {context_knowledge_content}
    
    [STYLE]
    {style_guide_content}

    [OUTLINE]
    {outline}
    
    [INSTRUCTIONS]
    Write a section of a blog post about {title}.
    Connect {title} to [GOALS] and [KNOWLEDGE] using [STYLE].
    Today's date is {current_date}.
    I need you to write ONLY the following section from [OUTLINE]:
    {section_title}
    
    Section description: {section_description}
    
    Target length for this section: approximately {approx_section_words} words

    Focus ONLY on writing this section - do not include other sections or a full blog post.
    Do not include the heading in your response - just write the content for this section.
    """
    return prompt

def get_random_post_length(min_words=4000, max_words=6000):
    """Generate a random word count for blog posts within the specified range."""
    return random.randint(min_words, max_words)

def generate_outline(client, args):
    """Generate an outline for the blog post."""
    try:
        outline_prompt = create_blog_prompt(args)
        outline_response = generate_content(client, outline_prompt, temperature=0.7, is_outline=True)
        
        # Ensure outline has proper heading format with ## for sections
        lines = outline_response.strip().split('\n')
        formatted_lines = []
        has_sections = False
        
        # Process the outline to ensure proper formatting
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append('')
                continue
                
            # Make sure section headers start with ##
            if line.lower().startswith(('section', 'part', 'body', 'main point')) and not line.startswith('#'):
                line = '## ' + line
                has_sections = True
            elif line.startswith('# ') or line.startswith('##'):
                has_sections = True
                
            formatted_lines.append(line)
            
        # If no section headers were found, try to add some based on the content
        if not has_sections:
            print("Warning: No clear section headers found in outline. Attempting to structure content...")
            new_outline = []
            title_added = False
            
            for line in formatted_lines:
                if line and not title_added and not line.startswith('#'):
                    # First non-empty line is the title
                    new_outline.append(line)  # Keep the title as is
                    title_added = True
                elif line and title_added and not line.startswith('#'):
                    # Convert non-header lines to section headers
                    if len(line.split()) <= 8:  # Short lines are likely section headers
                        new_outline.append(f"## {line}")
                    else:
                        # Long lines might be descriptions - try to extract a short header
                        section_name = ' '.join(line.split()[:4]) + '...'
                        new_outline.append(f"## {section_name}")
                        new_outline.append(line)  # Keep the original line as description
                else:
                    new_outline.append(line)
                    
            formatted_lines = new_outline
            
        formatted_outline = '\n'.join(formatted_lines)
        
        print("\n=== Blog Post Outline ===")
        print(formatted_outline)
        print("========================\n")
        
        return formatted_outline
        
    except Exception as e:
        print(f"Error generating outline: {e}")
        traceback.print_exc()
        
        # Return a basic outline structure as fallback
        fallback_outline = f"{args.topic}\n\n## Introduction\nIntroduction to the topic\n\n## Main Point 1\nFirst main point about the topic\n\n## Main Point 2\nSecond main point about the topic\n\n## Conclusion\nConclusion and summary"
        print("\n=== Fallback Outline (due to error) ===")
        print(fallback_outline)
        print("========================\n")
        return fallback_outline

def parse_outline(outline_text):
    """Parse the outline text into title and sections."""
    try:
        lines = outline_text.strip().split('\n')
        
        # Extract title (first non-empty line)
        title = None
        sections = []
        current_section = None
        description = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if not title:
                title = line.lstrip('#').strip()
                continue
                
            if line.startswith('##'):
                # Save previous section if exists
                if current_section:
                    # Clean the section title - keep only alphanumeric, periods, spaces, and emojis
                    # This regex keeps alphanumeric, periods, spaces, and emoji characters
                    clean_title = re.sub(r'[^:\w\s.\U0001F000-\U0001F9FF]', '', current_section)
                    sections.append({
                        'title': clean_title,
                        'description': ' '.join(description)
                    })
                    
                # Start new section
                current_section = line.lstrip('#').strip()
                description = []
            elif current_section and not line.startswith('#'):
                description.append(line)
        
        # Add the last section
        if current_section:
            # Clean the section title - keep only alphanumeric, periods, spaces, and emojis
            clean_title = re.sub(r'[^:\w\s.\U0001F000-\U0001F9FF]', '', current_section)
            sections.append({
                'title': clean_title,
                'description': ' '.join(description)
            })
        
        # Debug information
        print(f"Parsed outline - Title: {title}")
        print(f"Parsed outline - Sections: {len(sections)}")
        
        return title, sections
    except Exception as e:
        print(f"Error parsing outline: {e}")
        print(f"Raw outline text: {outline_text[:500]}...")
        raise

def generate_blog_post_sections(client, args, outline):
    """Generate each section of the blog post based on the outline."""
    try:
        title, sections = parse_outline(outline)
        
        if not title:
            print("Warning: No title found in the outline. Using topic as title.")
            title = args.topic
            
        if not sections:
            print("Warning: No sections found in the outline. Creating a default structure.")
            sections = [
                {'title': 'Introduction', 'description': 'Introduction to the topic'},
                {'title': 'Main Point 1', 'description': 'First main point about the topic'},
                {'title': 'Main Point 2', 'description': 'Second main point about the topic'},
                {'title': 'Conclusion', 'description': 'Conclusion and summary of the topic'}
            ]
            
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Generate each main section
        main_sections = []
        for i, section in enumerate(sections):
            print(f"Generating section {i+1}/{len(sections)}: {section['title']}")
            section_prompt = generate_section_prompt(
                title,
                section['title'],
                section['description'],
                outline,
                current_date,
                args.length,
                len(sections)
            )
            section_content = generate_content(client, section_prompt, temperature=0.7, is_outline=False)
            main_sections.append({
                'title': section['title'],
                'content': section_content
            })
        
        # Assemble the full blog post as HTML with article and section tags
        print("Assembling full blog post as HTML...")
        
        # Store the title separately for later use
        blog_title = title
        
        # Wordpress already includes the article title at top of page, so we don't need to add it here
        full_post = f'<article class="blog-post">\n'
        
        # Main content sections
        # openai will generate the introduction and conclusion sections, so we don't need to add them here
        for section in main_sections:
            # Create a clean section ID - replace non-alphanumeric with hyphens
            section_id = re.sub(r'[^a-zA-Z0-9]', '-', section['title'].lower())
            # Remove any consecutive hyphens and trim hyphens from start/end
            section_id = re.sub(r'-+', '-', section_id).strip('-')
            
            full_post += f'<section class="content-section" id="{section_id}">\n'
            full_post += f'<h2>{section["title"]}</h2>\n'
            full_post += section['content'] + '\n'
            full_post += '</section>\n\n'
        
        # Close article tag
        full_post += '</article>'
        
        print(f"HTML blog post generated successfully. Total length: ~{len(full_post.split())} words")
        
        # Return both the full post content and the title
        return full_post, blog_title
    except Exception as e:
        print(f"Error generating blog post sections: {e}")
        traceback.print_exc()
        raise

def generate_content(client, prompt, temperature=0.7, is_outline=False):
    """Generate content using OpenAI API."""
    try:
        print("Sending request to OpenAI API...")
        
        try:
            # Use different system prompts for outline generation versus content generation
            if is_outline:
                system_prompt = "You are a professional writer for a prestigious institution with expertise in cryptocurrency, DeFi, and creating persuasive marketing content that drives action. For outlining, use ONLY plain text or markdown formatting with ## for section headers. Be creative and use your own words and style. Do not use boring headers like 'Introduction' or 'Conclusion' or 'Call to Action'. DO NOT use HTML tags or formatting in outlines."
            else:
                system_prompt = "You are a professional writer for a prestigious institution with expertise in cryptocurrency, DeFi, and creating persuasive marketing content that drives action. Format your output in clean HTML using ONLY these tags: <p> for paragraphs, <h2> and <h3> for headings, <strong> or <b> for bold text, <em> or <i> for italics, <ul>/<ol> with <li> for lists, and <a> for links. Do not use any other HTML tags."
            
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            
            # Extract the response content
            content = response.choices[0].message.content.strip()
            
            print(f"OpenAI response received - length: {len(content)} characters")
            
            # Only post-process for HTML if not generating an outline
            if not is_outline:
                # Post-process to ensure proper HTML formatting for WordPress
                
                # Convert any markdown headings to HTML if they still exist
                content = re.sub(r'##\s+(.+?)\s*$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
                content = re.sub(r'###\s+(.+?)\s*$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
                
                # Convert any markdown paragraphs to HTML paragraphs if not already wrapped
                if '<p>' not in content:
                    # Split by double newlines to get paragraphs
                    paragraphs = re.split(r'\n\n+', content)
                    # Filter out empty paragraphs and wrap in <p> tags
                    paragraphs = ['<p>' + p.replace('\n', ' ') + '</p>' for p in paragraphs if p.strip()]
                    content = '\n\n'.join(paragraphs)
                
                # Convert any markdown lists to HTML lists
                # Unordered lists
                if re.search(r'(?m)^[-*]\s+', content):
                    content = re.sub(r'(?m)^[-*]\s+(.+?)$', r'<li>\1</li>', content)
                    content = re.sub(r'(?s)<li>.*?</li>', r'<ul>\g<0></ul>', content)
                
                # Ordered lists
                if re.search(r'(?m)^\d+\.\s+', content):
                    content = re.sub(r'(?m)^\d+\.\s+(.+?)$', r'<li>\1</li>', content)
                    content = re.sub(r'(?s)<li>.*?</li>', r'<ol>\g<0></ol>', content)
                
                # Convert markdown links to HTML links if any remain
                content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', content)
                
                # Convert markdown emphasis to HTML
                content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
                content = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', content)
                
                # Bold key terms related to the cryptocurrency
                content = re.sub(r'CL8Y(?![^<]*>)', r'<strong>CL8Y</strong>', content)
                content = re.sub(r'irreversible liquidity burn(?![^<]*>)', r'<strong>irreversible liquidity burn</strong>', content)
                content = re.sub(r'deflationary mechanics(?![^<]*>)', r'<strong>deflationary mechanics</strong>', content)
            
            return content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            traceback.print_exc()
            raise
    except Exception as e:
        print(f"Error in generate_content: {e}")
        traceback.print_exc()
        raise

def extract_title(content):
    """Extract the title from the generated content."""
    # Handle if content is a tuple (content, title)
    if isinstance(content, tuple) and len(content) == 2:
        return content[1]  # Return the title part of the tuple
    
    # Look for the first heading or the first line
    import re
    
    # Check if content is HTML or markdown
    is_html = '<html' in content.lower() or '<body' in content.lower() or '<article' in content.lower()
    
    if is_html:
        # Try to find heading tags (h1, h2, h3)
        heading_match = re.search(r'<h[1-3][^>]*>(.*?)</h[1-3]>', content, re.IGNORECASE | re.DOTALL)
        if heading_match:
            return heading_match.group(1).strip()
        
        # If no heading tag, look for a strong tag
        strong_match = re.search(r'<strong>(.*?)</strong>', content, re.IGNORECASE | re.DOTALL)
        if strong_match:
            return strong_match.group(1).strip()
    else:
        # Try to find markdown headings
        heading_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
        if heading_match:
            return heading_match.group(1).strip()
            
        # Look for the first non-empty line
        lines = content.strip().split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                return line.strip()
    
    # As a fallback, use the first line, cleaning any tags
    first_line = content.split('\n')[0]
    clean_line = re.sub(r'<[^>]+>', '', first_line).strip()
    
    if clean_line:
        return clean_line
    
    # If all else fails
    return "AI Generated Blog Post"

def save_to_file(content, filename=None):
    """Save the generated content to a file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"blog_post_{timestamp}.html"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Content saved to {filename}")
    return filename

def generate_meta_content(client, title, content, max_keyphrases=5):
    """Generate meta description and keyphrases for SEO using OpenAI."""
    try:
        # Extract plain text from HTML content for better processing
        plain_text = re.sub(r'<[^>]+>', '', content)
        # Limit to first 2000 chars to avoid token limits
        plain_text = plain_text[:2000] + "..." if len(plain_text) > 2000 else plain_text
        
        # Get current date for context
        current_date = datetime.now().strftime("%B %d, %Y")
        
        prompt = f"""
        Based on the following blog post title and content, generate:
        1. A compelling meta description (150-160 characters maximum)
        2. A list of {max_keyphrases} relevant keyphrases for SEO purposes
        
        Today's date is {current_date}. Please ensure the meta description and keyphrases are relevant and timely.
        
        Title: {title}
        
        Content excerpt:
        {plain_text}
        
        Format your response as JSON:
        {{
            "meta_description": "your meta description here",
            "keyphrases": ["keyphrase1", "keyphrase2", "keyphrase3", "keyphrase4", "keyphrase5"]
        }}
        
        Ensure the meta description is compelling, accurately summarizes the content, and is 150-160 characters.
        The keyphrases should be specific, relevant to the content, and have search value.
        """
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are an SEO expert who specializes in creating effective meta descriptions and keyphrases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        meta_content = json.loads(response.choices[0].message.content)
        
        # Validate and clean the response
        if 'meta_description' not in meta_content or 'keyphrases' not in meta_content:
            raise ValueError("Invalid response format from OpenAI")
        
        # Ensure meta description length
        meta_description = meta_content['meta_description']
        if len(meta_description) > 160:
            meta_description = meta_description[:157] + "..."
        
        # Ensure we have keyphrases
        keyphrases = meta_content['keyphrases']
        if not keyphrases or not isinstance(keyphrases, list):
            keyphrases = [title.lower()]
        
        return {
            'meta_description': meta_description,
            'keyphrases': keyphrases
        }
        
    except Exception as e:
        print(f"Error generating meta content: {e}")
        # Fallback to basic meta description and keyphrases
        return {
            'meta_description': f"{title} - Learn more about this topic in our detailed blog post.",
            'keyphrases': [title.lower()]
        }

def ensure_category_exists(headers, category_name):
    """
    Check if a category exists in WordPress using REST API.
    Returns the category ID if it exists, None if it doesn't or if there's an error.
    """
    if not category_name or category_name.strip() == "":
        print("Warning: Empty category name provided")
        return None
    
    category_name = category_name.strip()
    
    try:
        # Get all categories - using unauthenticated request since that works on this site
        print("Getting categories (unauthenticated since that works on this site)...")
        
        # First attempt: Try without authentication since the error message showed this works
        categories_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/categories?per_page=100"
        print(f"Requesting: {categories_url} (unauthenticated)")
        response = requests.get(categories_url)  # No headers = unauthenticated request
        
        # Debug information
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            categories = response.json()
            print(f"Successfully got {len(categories)} categories without authentication.")
            
            # Check if category exists (case-insensitive)
            for category in categories:
                if category['name'].lower() == category_name.lower():
                    print(f"Category '{category_name}' exists with ID: {category['id']}")
                    return category['id']
            
            # If we want to search more specifically
            print(f"Category '{category_name}' not found in first page. Trying with search parameter...")
            search_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/categories?search={category_name}&per_page=100"
            print(f"Requesting: {search_url} (unauthenticated)")
            search_response = requests.get(search_url)  # No headers = unauthenticated
            
            if search_response.status_code == 200:
                search_results = search_response.json()
                print(f"Search returned {len(search_results)} results")
                
                for category in search_results:
                    if category['name'].lower() == category_name.lower():
                        print(f"Category '{category_name}' found by search with ID: {category['id']}")
                        return category['id']
            
            # Try by slug as a last resort
            slug = category_name.lower().replace(' ', '-')
            slug_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/categories?slug={slug}"
            print(f"Trying by slug: {slug_url} (unauthenticated)")
            slug_response = requests.get(slug_url)
            
            if slug_response.status_code == 200:
                slug_results = slug_response.json()
                if slug_results and len(slug_results) > 0:
                    print(f"Category found by slug with ID: {slug_results[0]['id']}")
                    return slug_results[0]['id']
        else:
            print(f"Error fetching categories: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}...")  # Print first 200 chars of response
            
        # If we get here, we couldn't find the category
        print(f"No matching category found for '{category_name}'")
            
    except Exception as e:
        print(f"Error checking category: {e}")
        print("Will try to continue without category verification.")
        
    # If getting to this point, it means we couldn't find the category or had errors
    # Let's try creating the category if the user wants to post anyway
    try_create = input(f"Category '{category_name}' not found. Would you like to create it? (y/n): ")
    if try_create.lower() == 'y':
        return create_category(headers, category_name)
    
    # If user doesn't want to create it, suggest using Uncategorized
    print("Will attempt to use 'Uncategorized' category instead.")
    return None

def create_category(headers, category_name):
    """Attempt to create a new category in WordPress."""
    try:
        create_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/categories"
        create_data = {
            'name': category_name,
            'slug': category_name.lower().replace(' ', '-')
        }
        
        print(f"Attempting to create category: {category_name}")
        response = requests.post(create_url, headers=headers, json=create_data)
        
        if response.status_code in [200, 201]:
            new_category = response.json()
            print(f"Successfully created category '{category_name}' with ID: {new_category['id']}")
            return new_category['id']
        else:
            print(f"Failed to create category: HTTP {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return None
    except Exception as e:
        print(f"Error creating category: {e}")
        return None

def post_to_wordpress(title, content, category_name=None, category_id=None, tags=None, status="draft", meta_content=None, auth_method=None, use_application_password=False, debug=False):
    """Post the generated content to WordPress using the REST API.
    
    Category handling priority:
    1. If category_id is provided, it will be used directly (bypassing any name lookup)
    2. If only category_name is provided, the function will try to find its ID
    3. If category lookup fails, it will fall back to using Uncategorized
    """
    # Get headers for authentication
    headers = get_wordpress_headers(auth_method, use_application_password)
    
    # Use category name for WordPress
    if category_id:
        print(f"Using category ID: {category_id} (bypassing name lookup)")
    else:
        print(f"Using category name: {category_name}")
    
    # Ensure category_name is not empty if we don't have an ID
    if not category_id and (not category_name or category_name.strip() == ""):
        print("Warning: Empty category name provided, using 'Uncategorized' instead")
        category_name = "Uncategorized"
    
    # Only look up category ID if not directly provided and we have a name
    if not category_id:
        # Special handling for CL8Y News if that's the category having issues
        if category_name == "CL8Y News":
            print("Special handling for CL8Y News category - bypassing verification")
            # Ask the user if they know the category ID directly
            known_id = input("Do you know the ID for the 'CL8Y News' category? Enter the ID or press Enter to skip: ")
            if known_id and known_id.isdigit():
                category_id = int(known_id)
                print(f"Using provided ID {category_id} for CL8Y News")
            else:
                # Try a direct approach
                print("Will continue without category verification")
        else:
            # Standard approach - ensure the category exists
            category_id = ensure_category_exists(headers, category_name)
        
        # If category doesn't exist but is not Uncategorized, ask user if they want to continue
        if category_id is None and category_name != "Uncategorized":
            print("Warning: Could not verify category existence")
            choice = input("Do you want to (1) continue without the category, (2) use Uncategorized, or (3) abort? (1/2/3): ")
            
            if choice == "3":
                print("Aborting post creation")
                raise ValueError("Post creation aborted by user")
            elif choice == "2":
                category_name = "Uncategorized"
                print("Using 'Uncategorized' category instead")
                # Try one more time with Uncategorized
                category_id = ensure_category_exists(headers, "Uncategorized")
            else:
                print("Continuing without category verification")
                # We'll try to use the category name as provided but without ID verification
    
    # Convert tag strings to tag IDs
    try:
        tag_ids = []
        if tags:
            # Get existing tags
            tags_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/tags"
            response = requests.get(tags_url, headers=headers)
            
            if response.status_code == 200:
                existing_tags = response.json()
                existing_tag_dict = {tag['name'].lower(): tag['id'] for tag in existing_tags}
                
                # Check each tag and create it if it doesn't exist
                for tag_name in tags:
                    tag_name = tag_name.strip()
                    if not tag_name:
                        continue
                        
                    if tag_name.lower() in existing_tag_dict:
                        tag_ids.append(existing_tag_dict[tag_name.lower()])
                    else:
                        # Create new tag
                        new_tag_data = {'name': tag_name}
                        create_response = requests.post(tags_url, headers=headers, json=new_tag_data)
                        
                        if create_response.status_code in [200, 201]:
                            new_tag = create_response.json()
                            tag_ids.append(new_tag['id'])
                            print(f"Created new tag: {tag_name}")
                        else:
                            print(f"Failed to create tag {tag_name}: {create_response.status_code}")
            else:
                print(f"Error fetching tags: HTTP {response.status_code}")
                print("Will continue without tags")
    except Exception as e:
        print(f"Error processing tags: {e}")
        print("Will continue without tags")
    
    # Prepare post data
    post_data = {
        'title': title,
        'content': content,
        'status': status
    }
    
    # Only add categories if we have a valid category ID or we're using a name-based approach
    if category_id:
        post_data['categories'] = [category_id]
    elif category_name and category_name != "Uncategorized":
        # Try other approaches for categories
        if category_name == "CL8Y News":
            # Try sending the name directly - sometimes works
            post_data['categories_by_name'] = ["CL8Y News"]
            print("Using categories_by_name approach for CL8Y News")
        else:
            # Try string-based category assignment as fallback
            post_data['categories_by_name'] = [category_name]
    
    # Add tags if available
    if tag_ids:
        post_data['tags'] = tag_ids
    
    # Add meta description and keyphrases if available
    if meta_content:
        # Use the wp_add_meta module to add metadata
        post_data = wp_add_meta.add_meta_to_post_data(post_data, title, content, meta_content)
    
    # Send the request
    try:
        posts_url = f"{WP_URL.rstrip('/')}/wp-json/wp/v2/posts"
        print(f"Posting to WordPress: {posts_url}")
        print(f"Post data keys: {list(post_data.keys())}")
        
        # Debug information for SEO metadata
        if 'meta' in post_data:
            print("\nSEO Metadata being sent:")
            # Show all yoast fields in debug mode, otherwise just show the main ones
            if debug:
                print("FULL SEO METADATA:")
                for key, value in post_data['meta'].items():
                    print(f"  {key}: {value[:50]}..." if isinstance(value, str) and len(value) > 50 else f"  {key}: {value}")
            else:
                # In normal mode, just show most important fields
                for key, value in post_data['meta'].items():
                    if key.startswith('_yoast'):
                        if key in ['_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw', '_yoast_wpseo_title']:
                            print(f"  {key}: {value[:50]}..." if isinstance(value, str) and len(value) > 50 else f"  {key}: {value}")
            
            # In debug mode, also print the complete post_data structure
            if debug:
                print("\nDEBUG - Full post_data structure:")
                # Safely print the post_data with sensitive data masked
                safe_post_data = post_data.copy()
                if 'content' in safe_post_data:
                    safe_post_data['content'] = f"[Content length: {len(safe_post_data['content'])} chars]"
                print(json.dumps(safe_post_data, indent=2, default=str))
                
                # Check if REST API is properly configured
                print("\nDEBUG - Checking WordPress REST API configuration...")
                try:
                    # Test with a simpler endpoint first
                    test_url = f"{WP_URL.rstrip('/')}/wp-json"
                    print(f"Testing basic REST API at {test_url}")
                    test_response = requests.get(test_url, timeout=10)
                    print(f"REST API base response: HTTP {test_response.status_code}")
                    
                    # Check for existence of Yoast endpoint
                    yoast_test_url = f"{WP_URL.rstrip('/')}/wp-json/yoast"
                    print(f"Testing Yoast API at {yoast_test_url}")
                    yoast_response = requests.get(yoast_test_url, timeout=10)
                    print(f"Yoast API response: HTTP {yoast_response.status_code}")
                    
                    if yoast_response.status_code in [200, 201]:
                        print("Yoast REST API appears to be available.")
                    else:
                        print("Yoast REST API might not be correctly configured or accessible.")
                        print("You may need to manually set SEO metadata in WordPress.")
                except Exception as e:
                    print(f"Error testing REST API: {e}")
                    print("API testing failed. This might indicate connectivity issues with your WordPress site.")
        
        # Try posting with current configuration
        response = requests.post(posts_url, headers=headers, json=post_data)
        
        # Check if response includes meta data in the response
        if response.status_code in [200, 201]:
            result = response.json()
            post_id = result['id']
            
            print("\nResponse metadata check:")
            if 'meta' in result:
                print("Meta data found in response")
                for key, value in result['meta'].items():
                    if key.startswith('_yoast'):
                        print(f"  {key}: {value[:50]}..." if isinstance(value, str) and len(value) > 50 else f"  {key}: {value}")
            else:
                print("No meta data found in response. This may be normal if the WordPress installation doesn't return meta fields.")
            
            # First verify if the metadata actually took
            metadata_verified = False
            if 'meta' in post_data and any(k.startswith('_yoast') for k in post_data['meta']):
                print("\nVerifying if metadata was properly set...")
                metadata_verified = wp_add_meta.verify_meta_data(WP_URL, post_id, headers, debug)
                
                if metadata_verified:
                    print("Metadata verification successful! Yoast SEO metadata was properly set.")
                else:
                    print("Metadata verification failed. Yoast SEO metadata might not be properly set.")
            
            # If metadata verification failed, try alternative methods
            if not metadata_verified and 'meta' in post_data and any(k.startswith('_yoast') for k in post_data['meta']):
                print("\nNo Yoast SEO meta data found in response. Trying alternative methods...")
                
                try:
                    # Try to update the post with metadata separately
                    meta_content_full = {
                        'title': title,
                        'content': content,
                        'meta_description': meta_content.get('meta_description', ''),
                        'keyphrases': meta_content.get('keyphrases', [])
                    }
                    
                    # Pass the post ID and meta content to wp_add_meta module for handling
                    meta_update_success = wp_add_meta.update_post_meta(
                        WP_URL, 
                        post_id, 
                        meta_content_full, 
                        headers,
                        debug
                    )
                    
                    if meta_update_success:
                        print("Successfully updated meta data using alternative methods.")
                        
                        # Verify one more time
                        print("\nVerifying metadata after update attempt...")
                        metadata_verified = wp_add_meta.verify_meta_data(WP_URL, post_id, headers, debug)
                        
                        if metadata_verified:
                            print("Metadata verification successful after update!")
                        else:
                            print("Metadata verification still failed after update.")
                            print("You may need to set the Yoast SEO metadata manually.")
                            print(f"Edit URL: {WP_URL.rstrip('/')}/wp-admin/post.php?post={post_id}&action=edit")
                    else:
                        print("All automated methods to update meta data failed.")
                        print("You will need to set the Yoast SEO metadata manually.")
                        print(f"Edit URL: {WP_URL.rstrip('/')}/wp-admin/post.php?post={post_id}&action=edit")
                except Exception as e:
                    print(f"Error updating meta data: {e}")
                    print("SEO meta data may not have been properly set. You might need to set it manually in WordPress.")
                
            # Return the post ID on successful post
            return post_id
        else:
            print(f"Error posting to WordPress: HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}...")  # Print first 500 chars of response
            return None
    except Exception as e:
        print(f"Error posting to WordPress: {e}")
        return None

def main():
    """Main entry point for the script."""
    try:
        # Parse command line arguments
        args = setup_argparse()
        
        # Handle version display
        if args.version:
            print(f"WordPress AI Blog Post Generator v{VERSION}")
            sys.exit(0)
        
        # Initialize OpenAI client
        client = connect_to_openai()
        
        # Loop for multiple post generations
        for i in range(args.loop):
            if args.loop > 1:
                print(f"\n=== Running iteration {i+1} of {args.loop} ===\n")
            
            # Load existing content or generate new
            if args.load_file:
                # Load content from file
                print(f"Loading content from file: {args.load_file}")
                with open(args.load_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Check if content might already be a tuple format from previous run
                    if isinstance(content, tuple) and len(content) == 2:
                        content, title = content
                    else:
                        title = extract_title(content)
            else:
                # Generate outline
                outline = generate_outline(client, args)
                
                # Generate content based on outline
                content, title = generate_blog_post_sections(client, args, outline)
            
            # Save to file if requested
            if args.output_file:
                save_to_file(content, args.output_file)
            
            # Generate meta content if not skipped
            meta_content = None
            if not args.skip_meta:
                meta_content = generate_meta_content(client, title, content, args.keyphrases)
            
            # Post to WordPress if not skipped
            if not args.skip_post:
                post_id = post_to_wordpress(
                    title, 
                    content, 
                    category_name=args.category_name,
                    category_id=args.category_id,
                    tags=args.tags.split(',') if args.tags else DEFAULT_TAGS,
                    status=args.status,
                    meta_content=meta_content,
                    auth_method=args.auth_method,
                    use_application_password=args.use_application_password,
                    debug=args.debug
                )
                
                if post_id:
                    print(f"\nSuccessfully posted to WordPress with ID: {post_id}")
                    print(f"Edit URL: {WP_URL.rstrip('/')}/wp-admin/post.php?post={post_id}&action=edit")
                else:
                    print("\nFailed to post to WordPress. Content was generated but not posted.")
            
            # Wait between iterations if running multiple
            if args.loop > 1 and i < args.loop - 1:
                delay = random.randint(5, 15)
                print(f"\nWaiting {delay} seconds before next iteration...")
                time.sleep(delay)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 