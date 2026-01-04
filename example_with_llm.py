"""
Example of using the X Post Creator with LLM API integration.

This example shows how the service uses Claude or GPT-4 to create
more natural and engaging posts.
"""

import sys
import os

# Add src to path for direct execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from egile_mcp_x_post_creator.x_service import XPostService


def main():
    """Run LLM-powered post creation examples."""
    service = XPostService()
    
    print("=" * 70)
    print("X Post Creator - LLM-Powered Examples")
    print("=" * 70)
    
    # Check if LLM is available
    if service._has_anthropic:
        print("\n✅ Using: Anthropic Claude")
    elif service._has_openai:
        print("\n✅ Using: OpenAI GPT-4")
    else:
        print("\n⚠️  No LLM API key found - using simple generation")
        print("💡 Add ANTHROPIC_API_KEY or OPENAI_API_KEY to .env for better results")
    
    # Example scenarios
    examples = [
        {
            "title": "Product Launch Announcement",
            "text": "We just launched our new AI-powered analytics dashboard that helps businesses make better data-driven decisions in real-time",
            "style": "professional"
        },
        {
            "title": "Team Milestone",
            "text": "Our engineering team just hit 10,000 commits! So proud of what we've built together",
            "style": "casual"
        },
        {
            "title": "Tech Humor",
            "text": "You know you're a programmer when you spend 3 hours debugging only to find you forgot a semicolon",
            "style": "witty"
        },
        {
            "title": "Monday Motivation",
            "text": "Every line of code you write today is a step toward mastery. Keep building, keep learning, keep growing",
            "style": "inspirational"
        },
        {
            "title": "Conference Announcement",
            "text": "Speaking at TechConf 2026 next week about building scalable AI systems. Would love to see you there!",
            "style": "professional"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'-' * 70}")
        print(f"\n📝 Example {i}: {example['title']}")
        print(f"Style: {example['style']}")
        print(f"\n💭 Input:")
        print(f"   {example['text']}")
        
        result = service.create_post(
            text=example['text'],
            style=example['style'],
            include_hashtags=True,
            max_length=280
        )
        
        if result['success']:
            print(f"\n✨ Generated Post:")
            print(f"\n   {result['post_text'].replace(chr(10), chr(10) + '   ')}")
            print(f"\n📊 Stats:")
            print(f"   • Characters: {result['stats']['character_count']}/280")
            print(f"   • Hashtags: {result['stats']['hashtag_count']}")
            print(f"   • Emojis: {result['stats']['emoji_count']}")
        else:
            print(f"\n❌ Error: {result['error']}")
    
    print(f"\n{'=' * 70}")
    
    # Show comparison if LLM is available
    if service._has_anthropic or service._has_openai:
        print("\n🎯 LLM vs Simple Generation Comparison")
        print("=" * 70)
        
        test_text = "Just shipped a major update to our platform with improved performance"
        
        # LLM version
        print("\n🤖 LLM-Generated:")
        result = service.create_post(test_text, style="professional")
        if result['success']:
            print(f"   {result['post_text'].replace(chr(10), chr(10) + '   ')}")
        
        # Simple version (temporarily disable LLM)
        print("\n📝 Simple Generation:")
        has_anthropic = service._has_anthropic
        has_openai = service._has_openai
        service._has_anthropic = False
        service._has_openai = False
        
        result = service.create_post(test_text, style="professional")
        if result['success']:
            print(f"   {result['post_text'].replace(chr(10), chr(10) + '   ')}")
        
        # Restore
        service._has_anthropic = has_anthropic
        service._has_openai = has_openai
        
        print(f"\n{'=' * 70}")
    
    print("\n✅ Examples completed!")
    print("\n💡 Tips:")
    print("   • LLM-powered posts are more natural and engaging")
    print("   • Try different styles to match your brand voice")
    print("   • Always review posts before publishing")
    print(f"\n{'=' * 70}\n")


if __name__ == "__main__":
    main()
