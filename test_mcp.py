"""
Test the MCP X Post Creator functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from egile_mcp_x_post_creator.x_service import XPostService


def test_post_creation():
    """Test creating posts with different styles."""
    service = XPostService()
    
    test_cases = [
        {
            "text": "Just launched our new AI-powered customer support feature!",
            "style": "professional",
            "include_hashtags": True
        },
        {
            "text": "Having an amazing day building cool stuff with Python!",
            "style": "casual",
            "include_hashtags": True
        },
        {
            "text": "Why did the programmer quit his job? He didn't get arrays!",
            "style": "witty",
            "include_hashtags": False
        },
        {
            "text": "Every expert was once a beginner. Keep learning, keep growing!",
            "style": "inspirational",
            "include_hashtags": True
        }
    ]
    
    print("=" * 70)
    print("Testing Post Creation")
    print("=" * 70)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test['style']} style ---")
        print(f"Input: {test['text']}")
        
        result = service.create_post(
            text=test['text'],
            style=test['style'],
            include_hashtags=test['include_hashtags']
        )
        
        if result['success']:
            print(f"\n✅ Success!")
            print(f"Output: {result['post_text']}")
            print(f"Stats: {result['stats']}")
        else:
            print(f"\n❌ Failed: {result['error']}")
    
    print("\n" + "=" * 70)


def test_publish_simulation():
    """Test the publish flow (without actually publishing)."""
    service = XPostService()
    
    print("\n" + "=" * 70)
    print("Testing Publish Flow (Simulation)")
    print("=" * 70)
    
    test_post = "🚀 Testing the X Post Creator MCP Server! #AI #Development"
    
    # Test without confirmation
    print("\n--- Test 1: Publish without confirmation ---")
    result = service.publish_post(test_post, confirm=False)
    print(f"Result: {result}")
    
    # Test with confirmation but no credentials
    print("\n--- Test 2: Publish with confirmation (no credentials) ---")
    result = service.publish_post(test_post, confirm=True)
    print(f"Result: {result}")
    
    print("\n" + "=" * 70)


def test_character_limit():
    """Test handling of long text."""
    service = XPostService()
    
    print("\n" + "=" * 70)
    print("Testing Character Limit Handling")
    print("=" * 70)
    
    long_text = """
    This is a very long text that exceeds the normal character limit for X/Twitter posts.
    We want to make sure that our service can handle this gracefully and truncate the text
    in a smart way that preserves complete words and doesn't cut off in the middle of a sentence.
    The service should add an ellipsis at the end to indicate that the text was truncated.
    Let's see how it handles this very long input text!
    """
    
    print(f"\nInput length: {len(long_text)} characters")
    
    result = service.create_post(
        text=long_text,
        style="professional",
        include_hashtags=True,
        max_length=280
    )
    
    if result['success']:
        print(f"\n✅ Success!")
        print(f"Output: {result['post_text']}")
        print(f"Output length: {result['stats']['character_count']} characters")
    else:
        print(f"\n❌ Failed: {result['error']}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("\n🧪 X Post Creator MCP Server - Test Suite\n")
    
    test_post_creation()
    test_character_limit()
    test_publish_simulation()
    
    print("\n✅ All tests completed!\n")
    print("Note: To actually publish posts, you need to:")
    print("  1. Set up X/Twitter API credentials in .env file")
    print("  2. Run: python -m egile_mcp_x_post_creator")
    print()
