"""
MCP Server for creating and publishing X/Twitter posts.
"""

import logging
import os

from mcp.server.fastmcp import FastMCP
from .x_service import XPostService

log_level = os.getenv("FASTMCP_LOG_LEVEL", os.getenv("LOG_LEVEL", "INFO")).upper()
log_file = os.getenv("MCP_LOG_FILE")

logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_file if log_file else None,
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("X Post Creator")
x_service = XPostService()
logger.info("MCP server module loaded (log_level=%s, log_file=%s)", log_level, log_file)


@mcp.tool()
def create_post(
    text: str | None = None,
    post_text: str | None = None,
    style: str = "professional",
    include_hashtags: bool = True,
    max_length: int = 280
) -> str:
    """
    Create an attractive X/Twitter post from input text.
    
    This tool transforms your input text into an engaging post optimized for X/Twitter,
    with style-specific formatting, emojis, and relevant hashtags.
    
    Args:
        text: The input text to transform into a post (required unless post_text provided).
        post_text: Alias for text; if provided, used as the input.
        style: Writing style to use (optional). Options:
               - "professional": Business-focused, polished tone
               - "casual": Friendly, conversational tone
               - "witty": Humorous, clever tone
               - "inspirational": Motivational, uplifting tone
               Default: "professional"
        include_hashtags: Whether to include relevant hashtags (optional).
                         Default: True
        max_length: Maximum character length for the post (optional).
                   Default: 280 (X's character limit)
    
    Returns:
        A formatted string containing the created post and its statistics.
        The post is ready to be published or further edited.
    
    Example:
        create_post(
            text="Just launched our new AI feature that helps automate customer support!",
            style="casual",
            include_hashtags=True
        )
        
        Returns a post like:
        "Hey! Just launched our new AI feature that helps automate customer support! ✨
        
        #AI #Innovation"
    """
    effective_text = text or post_text
    if not effective_text:
        return "❌ Error: No text provided. Pass either 'text' or 'post_text' with the content to draft."

    logger.info(
        "create_post called len=%s style=%s include_hashtags=%s max_length=%s",
        len(effective_text),
        style,
        include_hashtags,
        max_length,
    )

    result = x_service.create_post(effective_text, style, include_hashtags, max_length)
    
    if not result["success"]:
        return f"❌ Error: {result['error']}"
    
    stats = result["stats"]
    output = f"✅ Post Created Successfully!\n\n"
    output += f"📝 POST TEXT:\n{'-' * 60}\n"
    output += f"{result['post_text']}\n"
    output += f"{'-' * 60}\n\n"
    output += f"📊 STATISTICS:\n"
    output += f"  • Characters: {stats['character_count']}/{max_length}\n"
    output += f"  • Hashtags: {stats['hashtag_count']}\n"
    output += f"  • Emojis: {stats['emoji_count']}\n"
    output += f"  • URLs: {stats['url_count']}\n"
    output += f"  • Style: {result['style']}\n\n"
    output += f"💡 TIP: To publish this post, use the publish_post tool with confirm=True\n"
    
    return output


@mcp.tool()
def publish_post(post_text: str, confirm: bool = False) -> str:
    """
    Publish a post to X/Twitter.
    
    ⚠️ IMPORTANT: This tool will actually post to your X/Twitter account!
    Always review the post content carefully before publishing.
    
    SAFETY REQUIREMENT: You must explicitly set confirm=True to publish.
    This prevents accidental publishing.
    
    Args:
        post_text: The complete text of the post to publish (required).
                  This should be the exact text you want to appear on X/Twitter.
        confirm: Explicit confirmation to publish (required for publishing).
                Must be set to True to actually post. If False or omitted,
                the tool will return an error.
                Default: False
    
    Returns:
        A formatted string with the publish status, including:
        - Success/failure status
        - Link to the published post (if successful)
        - Error messages (if failed)
        - Setup instructions (if credentials not configured)
    
    Prerequisites:
        - X/Twitter API credentials must be configured in .env file
        - Your X/Twitter app must have write permissions
        - The account must be properly authenticated
    
    Example:
        # First create a post
        result = create_post("Exciting announcement coming soon!")
        
        # Then publish with explicit confirmation
        publish_post(
            post_text="🚀 Exciting announcement coming soon! #News",
            confirm=True  # Must be True to actually publish!
        )
    
    Security Notes:
        - This tool requires explicit confirmation to prevent accidental posts
        - Review the post_text carefully before confirming
        - Ensure your API credentials are kept secure in the .env file
        - Never share your .env file or commit it to version control
    """
    logger.info("publish_post called confirm=%s len_post=%s", confirm, len(post_text))

    result = x_service.publish_post(post_text, confirm)
    
    if not result["success"]:
        output = f"❌ Publish Failed\n\n"
        
        if result.get("requires_confirmation"):
            output += f"⚠️  CONFIRMATION REQUIRED\n"
            output += f"Error: {result['error']}\n\n"
            output += f"To publish this post, you must explicitly set confirm=True:\n"
            output += f"  publish_post(post_text=\"{post_text[:50]}...\", confirm=True)\n\n"
            output += f"⚠️  This is a safety feature to prevent accidental publishing!\n"
            
        elif result.get("requires_setup"):
            output += f"🔧 SETUP REQUIRED\n"
            output += f"Error: {result['error']}\n\n"
            output += f"To publish posts, you need to:\n"
            output += f"1. Get X/Twitter API credentials from: https://developer.twitter.com/\n"
            output += f"2. Add them to your .env file:\n"
            output += f"   X_API_KEY=your_api_key\n"
            output += f"   X_API_SECRET=your_api_secret\n"
            output += f"   X_ACCESS_TOKEN=your_access_token\n"
            output += f"   X_ACCESS_TOKEN_SECRET=your_access_token_secret\n"
            
        else:
            output += f"Error: {result['error']}\n"
            if "details" in result:
                output += f"Details: {result['details']}\n"
        
        return output
    
    # Success!
    output = f"✅ POST PUBLISHED SUCCESSFULLY!\n\n"
    output += f"📝 Post Text:\n{post_text}\n\n"
    output += f"🔗 View your post at:\n{result['tweet_url']}\n\n"
    output += f"Tweet ID: {result['tweet_id']}\n"
    
    return output


if __name__ == "__main__":
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser(description="X Post Creator MCP Server")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio", "sse"],
        help="Transport protocol to use (stdio for Claude Desktop, sse for web apps)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for SSE server (only used with --transport sse)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE server (only used with --transport sse)"
    )
    
    args = parser.parse_args()
    
    if args.transport == "stdio":
        logger.info("Starting MCP server (stdio) host=%s port=%s", args.host, args.port)
        # Run with stdio transport for MCP clients like Claude Desktop
        mcp.run()
    elif args.transport == "sse":
        logger.info("Starting MCP server (sse) host=%s port=%s", args.host, args.port)
        # Run with SSE transport for web applications
        print(f"🚀 Starting X Post Creator MCP Server on {args.host}:{args.port}")
        print(f"📡 Transport: Server-Sent Events (SSE)")
        print(f"🔗 Access at: http://{args.host}:{args.port}")
        uvicorn.run(mcp.sse_app, host=args.host, port=args.port)
