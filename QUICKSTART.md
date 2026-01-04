# Quick Start Guide

Get up and running with X Post Creator in 5 minutes!

## 1. Install (2 minutes)

```bash
# Windows
cd egile-mcp-x-post-creator
.\install.bat

# Linux/Mac
cd egile-mcp-x-post-creator
chmod +x install.sh
./install.sh
```

## 2. Configure API Keys (2 minutes)

Edit `.env` file and add your keys:

### Required for Publishing
```bash
# Get from: https://developer.twitter.com/en/portal/dashboard
X_API_KEY=your_twitter_api_key
X_API_SECRET=your_twitter_api_secret
X_ACCESS_TOKEN=your_twitter_access_token
X_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
```

### Recommended for Best Results
```bash
# Get from: https://console.anthropic.com (recommended)
ANTHROPIC_API_KEY=your_anthropic_key

# OR from: https://platform.openai.com
OPENAI_API_KEY=your_openai_key
```

## 3. Test (1 minute)

```bash
# Run the example
python example_with_llm.py

# Or run the test suite
python test_mcp.py
```

## 4. Use It!

### From Python

```python
from egile_mcp_x_post_creator.x_service import XPostService

service = XPostService()

# Create a post
result = service.create_post(
    text="Just launched our amazing new feature!",
    style="casual"
)

print(result['post_text'])

# Publish (requires confirmation)
service.publish_post(
    post_text=result['post_text'],
    confirm=True
)
```

### As MCP Server

```bash
# For Claude Desktop or other MCP clients
python -m egile_mcp_x_post_creator

# For web apps (SSE)
python -m egile_mcp_x_post_creator --transport sse --port 8000
```

### With Egile Agent Core

```python
from egile_agent_core import Agent, AgentConfig
from egile_agent_core.plugins.mcp_plugin import MCPPlugin

agent = Agent(AgentConfig(name="Social Media Manager"))
agent.add_plugin(MCPPlugin(
    server_script_path="path/to/server.py"
))

agent.run("Create a post about our product launch")
```

## Quick Reference

### Styles
- `professional` - Business-focused, polished
- `casual` - Friendly, conversational
- `witty` - Humorous, clever
- `inspirational` - Motivational, uplifting

### Common Commands

```bash
# Create a professional post
create_post(text="Your text", style="professional")

# Create without hashtags
create_post(text="Your text", include_hashtags=False)

# Shorter post (for threads)
create_post(text="Your text", max_length=240)

# Publish (always with confirm=True)
publish_post(post_text="Your post", confirm=True)
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- See [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for more examples
- Check [LLM_INTEGRATION.md](LLM_INTEGRATION.md) for AI setup
- Review [INSTALL.md](INSTALL.md) for troubleshooting

## Common Issues

**No LLM key?** Posts still work, just use simple generation

**Publishing fails?** Check X API credentials and app permissions

**Module not found?** Activate virtual environment:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

## Support

Having issues? Check the documentation or open an issue on the repository.

---

**You're ready to create amazing posts! 🚀**
