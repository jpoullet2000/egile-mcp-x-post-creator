# Egile MCP X Post Creator

An MCP (Model Context Protocol) server that creates and publishes attractive X/Twitter posts.

## Features

- **create_post**: Generate engaging X/Twitter posts from input text
  - **AI-Powered**: Uses LLM APIs (Claude or GPT-4) for natural, compelling content
  - Multiple writing styles: professional, casual, witty, inspirational
  - Optimizes content for X's character limits
  - Adds relevant hashtags and emojis strategically
  - Falls back to rule-based generation if no API key configured

- **publish_post**: Publish posts to X/Twitter (requires user confirmation)
  - Integrates with X API
  - Always asks for permission before publishing
  - Returns post URL on success
  - Built-in safety checks

## Installation

### Prerequisites

- Python 3.10 or higher
- X/Twitter Developer Account (for publishing features)

### Setup

1. Clone or download this repository

2. Run the installation script:
   ```bash
   # On Windows
   install.bat
   
   # On Linux/Mac
   chmod +x install.sh
   ./install.sh
   ```

3. Copy `.env.example` to `.env` and fill in your credentials:
   ```bash
   cp .env.example .env
   ```

4. Get your X/Twitter API credentials from [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)

5. **(Recommended)** Add an LLM API key for better post generation:
   - Get an Anthropic API key from [console.anthropic.com](https://console.anthropic.com) (recommended)
   - OR get an OpenAI API key from [platform.openai.com](https://platform.openai.com)
   - Add to `.env`: `ANTHROPIC_API_KEY=your_key` or `OPENAI_API_KEY=your_key`

## Usage

### As an MCP Server

Run the server with stdio transport (for Claude Desktop or other MCP clients):

```bash
python -m egile_mcp_x_post_creator
```

Or with SSE transport for web applications:

```bash
python -m egile_mcp_x_post_creator --transport sse --host 0.0.0.0 --port 8000
```

### Available Tools

#### 1. create_post

Creates an attractive X/Twitter post from input text.

**Parameters:**
- `text` (required): The input text to transform into a post
- `style` (optional): Writing style - "professional", "casual", "witty", "inspirational" (default: "professional")
- `include_hashtags` (optional): Whether to include relevant hashtags (default: true)
- `max_length` (optional): Maximum character length (default: 280)

**Example:**
```python
create_post(
    text="Just launched our new AI-powered feature!",
    style="casual",
    include_hashtags=True
)
```

#### 2. publish_post

Publishes a post to X/Twitter. **Always requires user confirmation.**

**Parameters:**
- `post_text` (required): The text to publish
- `confirm` (required): Must be explicitly set to `true` to publish

**Dry run (no live tweet):** set `X_PUBLISH_DRY_RUN=true` in your environment to validate the call path without sending anything. The tool will still require `confirm=true` and will return a dry-run response with the echoed text.

**Example:**
```python
publish_post(
    post_text="🚀 Just launched our new AI-powered feature! #AI #Innovation",
    confirm=True
)
```
**X/Twitter API credentials** (required for publishing)
- **LLM API keys** (highly recommended for best results):
  - `ANTHROPIC_API_KEY` - Claude Sonnet 3.5 (recommended for creative writing)
  - `OPENAI_API_KEY` - GPT-4o (alternative option)
  - The service will try Anthropic first, then OpenAI, then fall back to simple generation
- **Default settings**
Edit the `.env` file to configure:

- X/Twitter API credentials (required for publishing)
- OpenAI or Anthropic API keys (optional, for enhanced post generation)
- Default settings for post creation

## Integration with Egile Agent Core

This MCP server can be used with the Egile Agent Core framework:

```python
from egile_agent_core import Agent, AgentConfig
from egile_agent_core.plugins.mcp_plugin import MCPPlugin

config = AgentConfig(
    name="X Post Creator Agent",
    instructions="You help create and publish engaging X/Twitter posts"
)

agent = Agent(config)
agent.add_plugin(MCPPlugin(server_script_path="path/to/egile-mcp-x-post-creator/src/egile_mcp_x_post_creator/server.py"))

# Use the agent
response = agent.run("Create a post about our new product launch")
```

## Requirements

See `pyproject.toml` for the complete list of dependencies.

## License

MIT License

## Support

For issues and questions, please open an issue on the repository.
