"""
Simple example of using the X Post Creator MCP Server
"""

import sys
import os

# Add src to path for direct execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from egile_mcp_x_post_creator.x_service import XPostService


def main():
    """Run example post creation."""
    print("=" * 70)
    print("X Post Creator - Example Usage")
    print("=" * 70)
    
    service = XPostService()
    
    # Example 1: Professional announcement
    print("\n📢 Example 1: Professional Announcement\n")
    print("Input: 'Excited to share that our team has grown to 50 people!'")
    
    result = service.create_post(
        text="Excited to share that our team has grown to 50 people!",
        style="professional",
        include_hashtags=True
    )
    
    if result['success']:
        print(f"\n✅ Generated Post:")
        print(f"{result['post_text']}")
        print(f"\n📊 Stats: {result['stats']}")
    
    # Example 2: Casual update
    print("\n" + "-" * 70)
    print("\n💬 Example 2: Casual Update\n")
    print("Input: 'Just deployed a new feature! Can't wait for everyone to try it!'")
    
    result = service.create_post(
        text="Just deployed a new feature! Can't wait for everyone to try it!",
        style="casual",
        include_hashtags=True
    )
    
    if result['success']:
        print(f"\n✅ Generated Post:")
        print(f"{result['post_text']}")
        print(f"\n📊 Stats: {result['stats']}")
    
    # Example 3: Inspirational quote
    print("\n" + "-" * 70)
    print("\n✨ Example 3: Inspirational Message\n")
    print("Input: 'The best time to start was yesterday. The next best time is now.'")
    
    result = service.create_post(
        text="The best time to start was yesterday. The next best time is now.",
        style="inspirational",
        include_hashtags=True
    )
    
    if result['success']:
        print(f"\n✅ Generated Post:")
        print(f"{result['post_text']}")
        print(f"\n📊 Stats: {result['stats']}")
    
    # Example 4: Test publish flow (without actually publishing)
    print("\n" + "-" * 70)
    print("\n🚀 Example 4: Publish Flow (Simulation)\n")
    
    test_post = "🎉 Testing the X Post Creator! #MCP #AI"
    print(f"Attempting to publish: {test_post}")
    
    # First, try without confirmation
    print("\n❌ Without confirmation:")
    result = service.publish_post(test_post, confirm=False)
    print(f"   {result.get('error', 'Unknown result')}")
    
    # Then, try with confirmation (but no credentials)
    print("\n⚠️  With confirmation (no credentials):")
    result = service.publish_post(test_post, confirm=True)
    print(f"   {result.get('error', 'Unknown result')}")
    
    print("\n" + "=" * 70)
    print("\n✅ Examples completed!")
    print("\n💡 To actually publish posts:")
    print("   1. Set up X/Twitter API credentials in .env")
    print("   2. Use: publish_post(post_text, confirm=True)")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
