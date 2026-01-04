# Egile MCP X Post Creator - Project Overview

## 🎯 Purpose

An MCP (Model Context Protocol) server that creates and publishes attractive X/Twitter posts using AI-powered generation. Perfect for automating social media content while maintaining quality and authenticity.

## ✨ Key Features

### 🤖 AI-Powered Post Generation
- **LLM Integration**: Uses Anthropic Claude or OpenAI GPT for natural content
- **Multiple Styles**: Professional, casual, witty, and inspirational tones
- **Smart Formatting**: Automatic emoji and hashtag placement
- **Character Limits**: Strict 280-character compliance with intelligent truncation

### 🔒 Safe Publishing
- **Confirmation Required**: Always asks before posting to X/Twitter
- **Preview Posts**: Review before publishing
- **Error Handling**: Graceful fallbacks and clear error messages

### 🔌 Flexible Integration
- **MCP Protocol**: Works with Claude Desktop and other MCP clients
- **Egile Agent Core**: Seamless plugin integration
- **Standalone Usage**: Direct Python API access
- **Web Service**: SSE transport for web applications

## 📁 Project Structure

```
egile-mcp-x-post-creator/
├── src/
│   └── egile_mcp_x_post_creator/
│       ├── __init__.py          # Package initialization
│       ├── __main__.py          # CLI entry point
│       ├── server.py            # MCP server with tools
│       └── x_service.py         # Core logic (LLM + X API)
│
├── Documentation/
│   ├── README.md                # Main documentation
│   ├── QUICKSTART.md           # 5-minute getting started
│   ├── INSTALL.md              # Detailed installation
│   ├── USAGE_EXAMPLES.md       # Code examples
│   └── LLM_INTEGRATION.md      # AI setup guide
│
├── Examples/
│   ├── example.py              # Basic usage
│   └── example_with_llm.py     # LLM-powered examples
│
├── Installation/
│   ├── install.bat             # Windows installer
│   ├── install.sh              # Linux/Mac installer
│   └── pyproject.toml          # Package configuration
│
├── Configuration/
│   ├── .env.example            # Environment template
│   └── .gitignore              # Git ignore rules
│
└── Testing/
    └── test_mcp.py             # Test suite
```

## 🛠️ Technologies

### Core
- **Python 3.10+**: Main programming language
- **FastMCP**: MCP server framework
- **Tweepy**: X/Twitter API client

### AI/LLM
- **Anthropic Claude**: Primary LLM (Sonnet 3.5)
- **OpenAI GPT**: Alternative LLM (GPT-4o)

### Infrastructure
- **python-dotenv**: Environment management
- **uvicorn**: ASGI server for SSE transport

## 🎨 MCP Tools

### 1. create_post
Generates an attractive X/Twitter post from input text.

**Parameters:**
- `text` (required): Input text to transform
- `style` (optional): "professional", "casual", "witty", "inspirational"
- `include_hashtags` (optional): Add relevant hashtags (default: true)
- `max_length` (optional): Character limit (default: 280)

**Returns:** Formatted post with statistics

### 2. publish_post
Publishes a post to X/Twitter with safety confirmation.

**Parameters:**
- `post_text` (required): Exact text to publish
- `confirm` (required): Must be `true` to actually post

**Returns:** Success status and post URL

## 🔄 Workflow

```
Input Text
    ↓
[LLM Analysis]
    ├→ Claude (if available)
    ├→ GPT-4 (if available)
    └→ Simple Generation (fallback)
    ↓
[Post Formatting]
    ├→ Add emojis
    ├→ Add hashtags
    └→ Ensure character limit
    ↓
[Preview]
    ↓
[User Confirmation]
    ↓
[Publish to X/Twitter]
    ↓
Return Post URL
```

## 💡 Use Cases

1. **Social Media Automation**
   - Schedule posts through an agent
   - Auto-generate content from blog posts
   - Create thread content

2. **Content Marketing**
   - Transform long-form content into tweets
   - A/B test different post styles
   - Maintain consistent brand voice

3. **Developer Tools**
   - Share code releases and updates
   - Announce new features
   - Build community engagement

4. **Personal Branding**
   - Create professional posts easily
   - Maintain active social presence
   - Share insights and knowledge

## 🚀 Quick Start

```bash
# 1. Install
./install.sh  # or install.bat on Windows

# 2. Configure .env
cp .env.example .env
# Add your API keys

# 3. Test
python example_with_llm.py

# 4. Run as MCP server
python -m egile_mcp_x_post_creator
```

## 🔐 Required Credentials

### For Post Creation (Recommended)
- **Anthropic API Key** (recommended) OR
- **OpenAI API Key** (alternative)
- Works without these, but results are basic

### For Publishing (Required)
- **X API Key & Secret**
- **X Access Token & Secret**
- App must have "Read and Write" permissions

## 📊 Performance

- **Post Generation**: ~1-3 seconds with LLM
- **Simple Generation**: ~0.1 seconds
- **Publishing**: ~1-2 seconds
- **Cost per Post**: ~$0.002-0.003 (LLM)

## 🔒 Security Features

1. **Explicit Confirmation**: No accidental publishing
2. **Environment Variables**: Secure credential storage
3. **No Hardcoded Secrets**: All keys in .env
4. **Error Sanitization**: Safe error messages
5. **.gitignore**: Prevents credential commits

## 🧪 Testing

```bash
# Run all tests
python test_mcp.py

# Run examples
python example.py
python example_with_llm.py

# Test as MCP server (stdio)
python -m egile_mcp_x_post_creator

# Test as web service (SSE)
python -m egile_mcp_x_post_creator --transport sse --port 8000
```

## 🤝 Integration Examples

### With Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "x-post-creator": {
      "command": "python",
      "args": ["-m", "egile_mcp_x_post_creator"],
      "cwd": "/path/to/egile-mcp-x-post-creator"
    }
  }
}
```

### With Egile Agent Core
```python
from egile_agent_core import Agent
from egile_agent_core.plugins.mcp_plugin import MCPPlugin

agent = Agent(AgentConfig(name="Social Media Agent"))
agent.add_plugin(MCPPlugin(
    server_script_path="path/to/server.py"
))
```

## 📈 Future Enhancements

- [ ] Image attachment support
- [ ] Thread creation tool
- [ ] Scheduling functionality
- [ ] Analytics integration
- [ ] Multi-account support
- [ ] Post templates library
- [ ] A/B testing features
- [ ] Engagement metrics

## 📚 Documentation

- **[README.md](README.md)**: Main documentation
- **[QUICKSTART.md](QUICKSTART.md)**: Get started in 5 minutes
- **[INSTALL.md](INSTALL.md)**: Detailed installation guide
- **[USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)**: Code examples
- **[LLM_INTEGRATION.md](LLM_INTEGRATION.md)**: AI setup and configuration

## 🐛 Troubleshooting

See [INSTALL.md](INSTALL.md) for common issues and solutions.

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please follow the contribution guidelines.

---

**Built with ❤️ for the Egile ecosystem**
