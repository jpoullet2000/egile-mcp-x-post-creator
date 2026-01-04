# Installation Guide

## Quick Start

### Windows

1. Open PowerShell or Command Prompt
2. Navigate to the project directory:
   ```bash
   cd egile-mcp-x-post-creator
   ```
3. Run the installation script:
   ```bash
   .\install.bat
   ```

### Linux/Mac

1. Open Terminal
2. Navigate to the project directory:
   ```bash
   cd egile-mcp-x-post-creator
   ```
3. Make the script executable and run it:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## Manual Installation

If you prefer to install manually:

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. Install the package:
   ```bash
   pip install -e .
   ```

4. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

## Configuration

### X/Twitter API Setup

To publish posts, you need X/Twitter API credentials:

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)

2. Create a new App (or use an existing one)

3. Generate the following credentials:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret

4. Make sure your app has **Read and Write** permissions

5. Add credentials to `.env` file:
   ```bash
   X_API_KEY=your_api_key_here
   X_API_SECRET=your_api_secret_here
   X_ACCESS_TOKEN=your_access_token_here
   X_ACCESS_TOKEN_SECRET=your_access_token_secret_here
   ```

### Optional: AI API Keys

For enhanced post generation (future feature), you can add:

```bash
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Verification

Test your installation:

```bash
python test_mcp.py
```

This will run a series of tests to verify the MCP server is working correctly.

## Running the Server

### As an MCP Server (for Claude Desktop, etc.)

```bash
python -m egile_mcp_x_post_creator
```

### As a Web Service (SSE)

```bash
python -m egile_mcp_x_post_creator --transport sse --port 8000
```

## Troubleshooting

### "Module not found" error

Make sure you're in the virtual environment:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

### "API credentials not configured" error

Make sure you've:
1. Copied `.env.example` to `.env`
2. Added your X/Twitter API credentials to `.env`
3. Restarted the server after adding credentials

### "Insufficient permissions" error when publishing

Your X/Twitter app needs **Read and Write** permissions. Check your app settings in the Twitter Developer Portal.

## Next Steps

After installation, see [README.md](README.md) for usage examples and API documentation.
