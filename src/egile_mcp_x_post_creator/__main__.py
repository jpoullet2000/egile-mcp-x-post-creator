"""
Entry point for running the MCP server as a module.
"""

from .server import mcp

if __name__ == "__main__":
    import sys
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
        mcp.run()
    elif args.transport == "sse":
        print(f"🚀 Starting X Post Creator MCP Server on {args.host}:{args.port}")
        uvicorn.run(mcp.sse_app, host=args.host, port=args.port)
