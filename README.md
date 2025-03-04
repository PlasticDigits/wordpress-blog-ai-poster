# WordPress AI Blog Post Generator

A Python script that uses OpenAI to generate blog posts and automatically posts them to WordPress.

## Features

- Generate blog posts on any topic using OpenAI's language models
- Automatically generate topics from current news using Tavily search API
- Customize post length, tone, and structure
- Use markdown files for context and style information
- Apply different writing styles and formatting preferences
- Post directly to WordPress or save as HTML files
- WordPress integration via XML-RPC API
- Configurable post settings (categories, tags, draft/publish status)
- Save and reuse style settings
- **Generate SEO meta descriptions and keyphrases automatically**

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/wordpress-blog-ai-poster.git
cd wordpress-blog-ai-poster
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:

```bash
cp .env.example .env
```

4. Edit the `.env` file to add your API keys and WordPress credentials.

## Configuration

### API Keys

You'll need the following API keys:

1. **OpenAI API Key**: Get this from [OpenAI's platform](https://platform.openai.com/)
2. **Tavily API Key**: Get this from [Tavily](https://tavily.com/) for automatic topic generation

### WordPress Configuration

For WordPress, you'll need:

1. Your WordPress site URL
2. Username
3. Application password (not your regular login password)

#### Getting an Application Password

1. Log in to your WordPress dashboard
2. Go to Users → Profile
3. Scroll down to "Application Passwords"
4. Enter a name (e.g., "AI Blog Generator")
5. Click "Add New Application Password"
6. Copy the generated password to your `.env` file

### Context and Style Files

The script uses markdown files for context and style:

1. **Context_Style.md**: Contains style guidelines for blog post generation
2. **Context_Knowledge.md**: Contains knowledge/facts for the blog content
3. **Context_Topics.md**: Contains guidelines for automatic topic generation
4. **Context_Goal.md**: Contains goals and objectives for the content

Edit these files to customize the output of your generated blog posts.

## Usage

### Basic Usage

Generate a blog post and post it as a draft to WordPress:

```bash
python wp_ai_poster.py --topic "Your Blog Topic Here"
```

### Automatic Topic Generation

Run without specifying a topic to automatically generate one based on current news:

```bash
python wp_ai_poster.py
```

The script will:

1. Generate a search query based on guidelines in Context_Topics.md
2. Search for recent articles using Tavily search API
3. Randomly select an article and generate a topic from it
4. Use that topic to create your blog post

### Command Line Options

#### Basic Content Options

```
--topic           Topic for the blog post (if not provided, a random topic will be generated)
--length          Target word count for the blog post (default: random 2000-2500)
--context         Additional context for the blog post (can be used multiple times)
--temperature     Temperature for AI generation (0.0-1.0, default: 0.7)
--no-research     Disable web research (research is enabled by default)
--model           OpenAI model to use [default: gpt-4-turbo]
```

#### WordPress Options

```
--skip-post               Skip posting to WordPress, just generate content
--category-name           WordPress category name (default varies)
--category-id             WordPress category ID (bypasses category name lookup)
--tags                    Comma-separated list of tags
--status                  Post status (draft, publish, pending, private) [default: draft]
--use-application-password Use WordPress Application Password for authentication
--auth-method             Authentication method to use (basic, jwt, application)
```

#### File Handling Options

```
--load-file       Load existing content from file instead of generating
--output-file     Save generated content to file
--skip-meta       Skip generating meta description and keyphrases
```

#### SEO Options

```
--keyphrases      Number of keyphrases to generate for SEO [default: 5]
```

#### Extra Options

```
--debug           Enable debug output
--version         Show version information
--loop            Number of times to run the script (default: 1)
```

### Style Customization

The script uses the Context_Style.md file to define the style of your blog posts. This includes:

1. **Tones**: informative, casual, professional, enthusiastic, humorous, technical, storytelling, persuasive
2. **Structures**: standard, listicle, how-to, comparison, question-answer, case-study, interview, review

You can edit the Context_Style.md file to customize these styles.

### Examples

Generate a blog post about AI with 10 SEO keyphrases:

```bash
python wp_ai_poster.py --topic "The Future of AI in Business" --keyphrases 10
```

Generate a blog post with custom context and save it to a file:

```bash
python wp_ai_poster.py --topic "Python Development Tips" --context "Include best practices for Python 3.10+" --output-file python_tips.html
```

Generate a blog post and publish it immediately:

```bash
python wp_ai_poster.py --topic "Quick Recipe: 5-Minute Breakfast Ideas" --status publish
```

Generate a completely random blog post based on news:

```bash
python wp_ai_poster.py
```

## Customizing Context and Style

### Context Files

The system uses several context files:

1. **Context_Style.md**: This file defines the style guide for your blog posts.
2. **Context_Knowledge.md**: This file contains factual information and knowledge.
3. **Context_Topics.md**: Guidelines for automatic topic generation.
4. **Context_Goal.md**: Contains goals and objectives for the content.

To customize, simply edit these files to include your preferred guidelines and knowledge base.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for generating draft content. Always review and edit AI-generated content before publishing to ensure quality, accuracy, and originality.

## SEO Features

The script automatically generates SEO metadata for your WordPress posts:

1. **Meta Descriptions**: Compelling, concise descriptions (150-160 characters) to improve search engine listings
2. **Focus Keyphrases**: Automatically generates SEO-friendly keyphrases based on your content
3. **WordPress SEO Plugin Support**: Adds metadata compatible with popular SEO plugins like Yoast SEO and All in One SEO

The SEO features work by:

- Analyzing your generated content
- Creating a tailored meta description that summarizes the post
- Identifying relevant keyphrases for better search engine ranking
- Automatically adding these to your WordPress post via custom fields

Control the number of generated keyphrases with the `--keyphrases` option.
