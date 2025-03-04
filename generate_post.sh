#!/bin/bash
# Script to easily generate WordPress blog posts using OpenAI

# Make sure the script is executable
# chmod +x generate_post.sh

# Check if python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3."
    exit 1
fi

# Check if the .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit the .env file with your API keys and WordPress credentials."
    exit 1
fi

# Check if requirements are installed
if ! pip list | grep -q "openai"; then
    echo "Installing required dependencies..."
    pip install -r requirements.txt
fi

# Display help info about WordPress authentication if requested
if [[ "$*" == *"--help"* ]] || [[ "$*" == *"-h"* ]]; then
    echo ""
    echo "Content Generation Options:"
    echo "-------------------------"
    echo "--topic [TOPIC]  Specify topic for blog post (if not provided, a random topic"
    echo "                will be automatically generated based on current news)"
    echo "--length [WORDS]  Target word count (default: random 2000-2500 words)"
    echo "--style [STYLE]   Use a specific style profile (or random if not specified)"
    echo "--temperature [0.0-1.0]  Control randomness (default: 0.7)"
    echo "--no-research     Disable web research (research is enabled by default)"
    echo ""
    echo "Style Options:"
    echo "-------------"
    echo "The script randomly selects a tone and structure if not specified:"
    echo ""
    echo "Available tones: informative, casual, professional, enthusiastic,"
    echo "                 humorous, technical, storytelling, persuasive"
    echo ""
    echo "Available structures: standard, listicle, how-to, comparison,"
    echo "                      question-answer, case-study, interview, review"
    echo ""
    echo "WordPress REST API Authentication Options:"
    echo "------------------------------------------"
    echo "--use-application-password  Use WordPress Application Passwords authentication"
    echo "--auth-method [basic|jwt|application]  Specify authentication method"
    echo ""
    echo "Category Handling for HTTP 500 Errors:"
    echo "-------------------------------------"
    echo "--category-id [ID]  Directly specify category ID (bypasses API lookup)"
    echo "--category-name [NAME]  Specify category by name"
    echo ""
    echo "If you encounter HTTP 500 errors with categories, try:"
    echo "1. Using Application Passwords (Settings > Security > Application Passwords in WordPress)"
    echo "2. Using the --category-id option instead of category name"
    echo "   - You can find category IDs in WordPress admin under Posts > Categories"
    echo "   - Look at the category edit URL: .../wp-admin/term.php?taxonomy=category&tag_ID=X"
    echo "3. Using --category-name 'Uncategorized' as a fallback"
    echo ""
fi

# Pass all arguments to the Python script
python3 wp_ai_poster.py "$@" 