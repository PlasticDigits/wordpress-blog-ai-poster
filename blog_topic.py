#!/usr/bin/env python3
"""
Blog Topic Generator

This module uses OpenAI and Tavily search to automatically generate blog topics
based on guidelines in Context_Topics.md.
"""

import os
import random
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    print("Warning: tavily-python not installed. Using fallback search method.")

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Tavily API Configuration
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    print("Warning: TAVILY_API_KEY not found in .env file. Using fallback search method.")

# Path to topics markdown file
CONTEXT_TOPICS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Context_Topics.md")
CONTEXT_GOAL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Context_Goal.md")
CONTEXT_KNOWLEDGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Context_Knowledge.md")
CONTEXT_STYLE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Context_Style.md")

def connect_to_openai():
    """Initialize OpenAI client."""
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key not found. Please set it in your .env file.")
    
    return OpenAI(api_key=OPENAI_API_KEY)

def read_markdown_file(file_path):
    """Read content from a markdown file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            print(f"Warning: File not found at {file_path}")
            return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def read_topics_guidelines():
    """Read the topics guidelines from the markdown file."""
    return read_markdown_file(CONTEXT_TOPICS_FILE)

def generate_search_query(openai_client, guidelines):
    """Generate a search query using OpenAI based on the guidelines."""
    try:
        # Get current date for context
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Add randomness to guidelines by potentially removing parts
        if guidelines: 
            # Split guidelines into paragraphs
            paragraphs = guidelines.split('\n\n')
            
            if len(paragraphs) > 1:
                # Keep a random subset of paragraphs (at least 1)
                keep_count = random.randint(1, max(1, len(paragraphs) - 1))
                selected_paragraphs = random.sample(paragraphs, keep_count)
                randomized_guidelines = '\n\n'.join(selected_paragraphs)
            else:
                # If only one paragraph, keep a random portion of it
                sentences = paragraphs[0].split('.')
                if len(sentences) > 3:
                    keep_count = random.randint(2, len(sentences) - 1)
                    selected_sentences = random.sample(sentences, keep_count)
                    randomized_guidelines = '.'.join(selected_sentences) + '.'
                else:
                    randomized_guidelines = guidelines
        else:
            randomized_guidelines = guidelines
        
        prompt = f"""
        Based on the following guidelines for blog topics, generate a specific news search query 
        that will find current and relevant articles.
        
        Today's date is {current_date}. IMPORTANT: Please generate a query that will find recent and timely news.
        Do NOT include a date in the query.
        
        Guidelines:
        {randomized_guidelines}
        
        Return ONLY the search query string, nothing else. Make it specific enough to find 
        interesting current news but general enough to return results.
        """
        
        # Randomly vary the temperature for more diverse results
        temperature = round(random.uniform(0.6, 0.9), 1)
        
        # Randomize the system prompt
        system_prompts = [
            "You are a research assistant helping to find interesting news topics for blog posts.",
            "You are a journalist looking for trending stories in technology and finance.",
            "You are a crypto enthusiast searching for the latest developments in blockchain.",
            "You are a libertarian researcher exploring topics related to freedom and decentralization.",
            "You are an open source advocate tracking developments in software and technology."
        ]
        system_prompt = random.choice(system_prompts)
        
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        
        print(f"Using temperature: {temperature}")
        print(f"Using system prompt: {system_prompt}")
        
        # Get the raw search query
        search_query = response.choices[0].message.content.strip()
        
        # Remove quotation marks and other grammatical marks
        search_query = search_query.replace('"', '').replace("'", "").replace(""", "").replace(""", "")
        search_query = search_query.replace(".", "").replace("!", "").replace("?", "").replace(":", "")
        
        print(f"Generated search query: {search_query}")
        return search_query
    
    except Exception as e:
        print(f"Error generating search query: {e}")
        return "latest cryptocurrency news memecoin open source liberty"

def search_using_tavily_api(query):
    """Search for articles using the Tavily API."""
    try:
        # First try using the Tavily Python client if available
        if TAVILY_AVAILABLE and TAVILY_API_KEY:
            client = TavilyClient(api_key=TAVILY_API_KEY)
            search_result = client.search(query=query, search_depth="advanced", include_answer=False, max_results=10)
            
            if search_result and "results" in search_result:
                print(f"Found {len(search_result['results'])} results via Tavily API")
                return search_result["results"]
            
        # Fall back to direct API call if client not available
        elif TAVILY_API_KEY:
            url = "https://api.tavily.com/search"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {TAVILY_API_KEY}"
            }
            payload = {
                "query": query,
                "search_depth": "advanced",
                "include_answer": False,
                "max_results": 10
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "results" in data:
                    results = data["results"]
                    print(f"Found {len(results)} results via Tavily API direct request")
                    return results
        
        # If we get here, we need to use the fallback
        raise Exception("Tavily search failed or returned no results")
        
    except Exception as e:
        print(f"Error using Tavily API: {e}")
        return None

def search_news(query):
    """Search for news articles using the generated query."""
    try:
        # First try with Tavily API
        articles = search_using_tavily_api(query)
        if articles:
            # Format the articles and filter out invalid ones
            formatted_articles = []
            for article in articles:
                # Get title and description with fallbacks
                title = article.get('title', '')
                description = article.get('content', article.get('raw_content', ''))
                
                # Skip articles with empty titles or descriptions
                if not title or not description or title == 'EOF':
                    continue
                
                # Clean up any trailing "EOF" markers
                if title.endswith('EOF'):
                    title = title.rstrip('EOF').strip()
                
                formatted_articles.append({
                    'title': title,
                    'description': description,
                    'url': article.get('url', ''),
                    'source': article.get('source', 'Tavily Search'),
                    'published_at': datetime.now().isoformat()  # Tavily doesn't provide dates
                })
            
            if formatted_articles:
                return formatted_articles
        
        # Fallback to a web search approach
        print("Using fallback search method...")
        
        # Create more relevant fallback results based on the query
        fallback_results = [
            {
                'title': f"Recent developments in {query}",
                'description': f"This article discusses the latest trends and developments in {query}.",
                'url': f"https://example.com/article-about-{query.replace(' ', '-')}",
                'source': 'Example News',
                'published_at': datetime.now().isoformat()
            },
            {
                'title': f"Analysis: The impact of {query} on the market",
                'description': f"An in-depth analysis of how {query} is affecting various sectors.",
                'url': f"https://example.com/analysis-{query.replace(' ', '-')}",
                'source': 'Financial Times',
                'published_at': datetime.now().isoformat()
            }
        ]
        
        print("Generated fallback search results")
        return fallback_results
        
    except Exception as e:
        print(f"Error searching news: {e}")
        # Return a minimal fallback result
        return [
            {
                'title': f"Discussion on {query}",
                'description': f"An exploration of recent trends in {query}.",
                'url': "https://example.com",
                'source': 'Example Source',
                'published_at': datetime.now().isoformat()
            }
        ]

def generate_blog_topic(openai_client, article, guidelines):
    """Generate a blog topic based on a news article using OpenAI."""
    try:
        # Get current date for context
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Read content from context files
        context_goal_content = read_markdown_file(CONTEXT_GOAL_FILE)
        context_knowledge_content = read_markdown_file(CONTEXT_KNOWLEDGE_FILE)
        context_style_content = read_markdown_file(CONTEXT_STYLE_FILE)
        
        prompt = f"""
        [GOALS]
        {context_goal_content}
        
        [KNOWLEDGE]
        {context_knowledge_content}
        
        [STYLE]
        {context_style_content}

        [TOPIC]
        Title: {article['title']}
        Description: {article['description']}

        [INSTRUCTIONS]
        Today's date is {current_date}. Connect [TOPIC] to [GOALS] and [KNOWLEDGE] using [STYLE].
        Generate a specific blog title related to [TOPIC] that would accomplish [GOALS] and align with [KNOWLEDGE] using [STYLE].
        Include a brief (2-3 sentence) description of what the article should cover. Make it engaging and aligned with [GOALS].
        Do not include the current year or date in the title. Keep the title short and concise.
        Optimize the title for SEO by being very short and concise using common search phrases.
        
        Format your response as:
        TITLE: [Your title here]
        DESCRIPTION: [Your brief description here]
        """
        
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a blog editor specialized in cryptocurrency, open source, and pro-liberty content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )
        
        topic_response = response.choices[0].message.content.strip()
        
        # Extract title and description
        title_match = topic_response.split("TITLE:", 1)[-1].split("DESCRIPTION:", 1)[0].strip()
        description = ""
        if "DESCRIPTION:" in topic_response:
            description = topic_response.split("DESCRIPTION:", 1)[-1].strip()
        
        return {
            'title': title_match,
            'description': description,
            'source_article': article
        }
    
    except Exception as e:
        print(f"Error generating blog topic: {e}")
        return {
            'title': article['title'],
            'description': "Generated topic based on current news.",
            'source_article': article
        }

def get_random_topic():
    """Main function to get a random blog topic based on news search."""
    try:
        # Initialize OpenAI client
        openai_client = connect_to_openai()
        
        # Read topic guidelines
        guidelines = read_topics_guidelines()
        
        # Generate search query
        search_query = generate_search_query(openai_client, guidelines)
        
        # Search for news
        articles = search_news(search_query)
        
        if not articles:
            print("No articles found. Using default topic.")
            return default_topic()
        
        # Validate articles before selection
        valid_articles = [
            article for article in articles 
            if article.get('title') and len(article.get('title', '')) > 5
            and article.get('description') and len(article.get('description', '')) > 20
        ]
        
        if not valid_articles:
            print("No valid articles found. Using default topic.")
            return default_topic()
        
        # Randomly select one article
        selected_article = random.choice(valid_articles)
        print(f"Selected article: {selected_article['title']}")
        
        # Generate blog topic based on the article
        topic = generate_blog_topic(openai_client, selected_article, guidelines)
        
        # Validate the generated topic
        if not topic.get('title') or len(topic.get('title', '')) < 10:
            print("Generated topic title is too short or invalid. Using default.")
            return default_topic(selected_article)
        
        print(f"Generated blog topic: {topic['title']}")
        return topic
        
    except Exception as e:
        print(f"Error in get_random_topic: {e}")
        return default_topic()

def default_topic(article=None):
    """Return a default topic when article search or topic generation fails."""
    current_date = datetime.now().strftime("%B %d, %Y")
    
    if article and article.get('title'):
        # Create a topic based on the article if we have one
        return {
            'title': f"Analysis: {article['title']}",
            'description': f"A detailed exploration of the implications and context behind this news as of {current_date}.",
            'source_article': article
        }
    else:
        # Completely default topic
        return {
            'title': "The Current State of Decentralized Finance",
            'description': f"An examination of DeFi trends and developments as of {current_date}, with a focus on implications for financial sovereignty and liberty."
        }

# Example usage
if __name__ == "__main__":
    topic = get_random_topic()
    print(f"\nGenerated Blog Topic:")
    print(f"Title: {topic['title']}")
    print(f"Description: {topic['description']}")
    if 'source_article' in topic:
        print(f"\nBased on article: {topic['source_article']['title']}")
        print(f"Source: {topic['source_article']['source']}")
        print(f"URL: {topic['source_article']['url']}") 