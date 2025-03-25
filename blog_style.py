#!/usr/bin/env python3
"""
Blog Style Definitions

This module defines various style templates for AI-generated blog posts.
It includes tone, structure, and formatting preferences.
"""

import os
import json

class BlogStyle:
    """Class to handle blog post styling and formatting."""
    
    # HTML templates for different post types
    HTML_TEMPLATES = {
        "standard": """
<h2>{title}</h2>
<p class="intro">{intro}</p>
{body}
<h3>Conclusion</h3>
<p>{conclusion}</p>
""",
        "listicle": """
<h2>{title}</h2>
<p class="intro">{intro}</p>
<ol>
{list_items}
</ol>
<p>{conclusion}</p>
""",
        "how-to": """
<h2>{title}</h2>
<p class="intro">{intro}</p>
<h3>What You'll Need</h3>
<ul>
{materials}
</ul>
<h3>Steps</h3>
<ol>
{steps}
</ol>
<h3>Tips</h3>
<ul>
{tips}
</ul>
<p>{conclusion}</p>
"""
    }
    
    def __init__(self):
        """Initialize the blog style with default settings."""
        self.style_data = {
            "tone": "persuasive",
            "structure": "standard",
            "formatting": {
                "headings": True,
                "bold_key_points": True,
                "use_lists": True,
                "include_images": False,
                "image_placement": "after_heading"
            },
            "html_elements": {
                "use_blockquotes": True,
                "use_tables": False,
                "use_code_blocks": False
            },
            "custom_css_classes": []
        }
        
        self.style_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles")
        
        # Create styles directory if it doesn't exist
        if not os.path.exists(self.style_directory):
            os.makedirs(self.style_directory)
    
    @property
    def tone(self):
        """Get the current tone."""
        return self.style_data["tone"]
    
    @property
    def structure(self):
        """Get the current structure."""
        return self.style_data["structure"]
    
    def set_tone(self, tone):
        """Set the tone of the blog post."""
        # Always set to persuasive tone
        self.style_data["tone"] = "persuasive"
        return True
    
    def set_structure(self, structure):
        """Set the structure of the blog post."""
        # Always set to standard structure
        self.style_data["structure"] = "standard"
        return True
    
    def enable_formatting_option(self, option, value=True):
        """Enable or disable a formatting option."""
        if option in self.style_data["formatting"]:
            self.style_data["formatting"][option] = value
            return True
        else:
            print(f"Warning: '{option}' is not a recognized formatting option.")
            return False
    
    def enable_html_element(self, element, value=True):
        """Enable or disable an HTML element."""
        if element in self.style_data["html_elements"]:
            self.style_data["html_elements"][element] = value
            return True
        else:
            print(f"Warning: '{element}' is not a recognized HTML element.")
            return False
    
    def add_custom_css_class(self, class_name):
        """Add a custom CSS class to be used in the HTML."""
        if class_name not in self.style_data["custom_css_classes"]:
            self.style_data["custom_css_classes"].append(class_name)
    
    def remove_custom_css_class(self, class_name):
        """Remove a custom CSS class."""
        if class_name in self.style_data["custom_css_classes"]:
            self.style_data["custom_css_classes"].remove(class_name)
    
    def load_style(self, style_name):
        """Load a predefined style from a JSON file."""
        style_file = os.path.join(self.style_directory, f"{style_name.lower().replace(' ', '_')}.json")
        
        if os.path.exists(style_file):
            try:
                with open(style_file, 'r', encoding='utf-8') as f:
                    style_data = json.load(f)
                    
                # Update style data with loaded values
                for key, value in style_data.items():
                    if key in self.style_data:
                        self.style_data[key] = value
                        
                print(f"Loaded style: {style_name}")
                return True
            except Exception as e:
                print(f"Error loading style: {e}")
                return False
        else:
            print(f"Style not found: {style_name}")
            return False
    
    def save_style(self, style_name):
        """Save the current style as a predefined style for future use."""
        style_file = os.path.join(self.style_directory, f"{style_name.lower().replace(' ', '_')}.json")
        
        try:
            with open(style_file, 'w', encoding='utf-8') as f:
                json.dump(self.style_data, f, indent=2)
            print(f"Saved style: {style_name}")
            return True
        except Exception as e:
            print(f"Error saving style: {e}")
            return False
    
    def get_available_styles(self):
        """Get a list of available predefined styles."""
        styles = []
        for file in os.listdir(self.style_directory):
            if file.endswith('.json'):
                styles.append(os.path.splitext(file)[0].replace('_', ' '))
        return styles
    
    def get_available_tones(self):
        """Get a list of available tones with descriptions."""
        return {"persuasive": "Convincing, compelling, and motivational. Uses rhetorical questions and calls to action."}
    
    def get_available_structures(self):
        """Get a list of available structures with descriptions."""
        return {"standard": "Classic blog structure with introduction, body paragraphs, and conclusion."}
    
    def get_style_for_prompt(self):
        """Format the style data for inclusion in an AI prompt."""
        prompt_style = "STYLE GUIDELINES:\n\n"
        
        # Add tone information
        tone = self.style_data["tone"]
        prompt_style += f"Tone: {tone.capitalize()}\n"
        prompt_style += f"Description: Convincing, compelling, and motivational. Uses rhetorical questions and calls to action.\n\n"
        
        # Add structure information
        structure = self.style_data["structure"]
        prompt_style += f"Structure: {structure.capitalize()}\n"
        prompt_style += f"Format: Classic blog structure with introduction, body paragraphs, and conclusion.\n\n"
        
        # Add formatting preferences
        prompt_style += "Formatting Preferences:\n"
        for option, value in self.style_data["formatting"].items():
            prompt_style += f"- {option.replace('_', ' ').capitalize()}: {'Yes' if value else 'No'}\n"
        
        # Add HTML element preferences
        prompt_style += "\nHTML Elements to Include:\n"
        for element, value in self.style_data["html_elements"].items():
            prompt_style += f"- {element.replace('_', ' ').capitalize()}: {'Yes' if value else 'No'}\n"
        
        # Add custom CSS classes if any
        if self.style_data["custom_css_classes"]:
            prompt_style += "\nCustom CSS Classes to Use:\n"
            for css_class in self.style_data["custom_css_classes"]:
                prompt_style += f"- {css_class}\n"
        
        return prompt_style
    
    def get_html_template(self):
        """Get the HTML template for the current structure."""
        structure = self.style_data["structure"]
        return self.HTML_TEMPLATES.get(structure, self.HTML_TEMPLATES["standard"])

def analyze_and_enhance(content, tone="persuasive"):
    """
    Analyze blog content and enhance it based on style guidelines.
    
    Args:
        content (str): The blog post content to enhance
        tone (str, optional): The tone to use for enhancement. Defaults to "persuasive".
        
    Returns:
        str: The enhanced blog content
    """
    # Create a style instance
    style = BlogStyle()
    
    # Set the tone (currently only persuasive is supported)
    style.set_tone(tone)
    
    # Get the style guidelines for potential future enhancements
    style_guidelines = style.get_style_for_prompt()
    
    # Currently, we're just returning the original content
    # In a future version, this function could apply more sophisticated 
    # enhancements based on style rules and NLP analysis
    
    return content

# Example usage
if __name__ == "__main__":
    style = BlogStyle()
    
    # Set tone and structure
    style.set_tone("casual")
    style.set_structure("listicle")
    
    # Configure formatting options
    style.enable_formatting_option("include_images", True)
    style.enable_html_element("use_tables", True)
    
    # Add custom CSS classes
    style.add_custom_css_class("featured-post")
    style.add_custom_css_class("highlight")
    
    # Get formatted style guidelines
    formatted_style = style.get_style_for_prompt()
    print(formatted_style)
    
    # Save the style for future use
    # style.save_style("casual_listicle") 