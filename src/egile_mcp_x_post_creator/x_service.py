"""
X/Twitter service for creating and publishing posts.
"""

import os
import re
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class XPostService:
    """Service for creating and publishing X/Twitter posts."""
    
    def __init__(self):
        """Initialize the X post service."""
        self.max_length = int(os.getenv("DEFAULT_MAX_LENGTH", "280"))
        self.include_hashtags_default = os.getenv("INCLUDE_HASHTAGS", "true").lower() == "true"
        self.dry_run = os.getenv("X_PUBLISH_DRY_RUN", "false").lower() == "true"
        
        # X API credentials (lazy loaded)
        self._twitter_client = None
        
        # LLM clients (lazy loaded)
        self._openai_client = None
        self._anthropic_client = None
        
        # Check which LLM APIs are available
        self._has_openai = bool(os.getenv("OPENAI_API_KEY"))
        self._has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    
    def create_post(
        self,
        text: str,
        style: str = "professional",
        include_hashtags: bool = True,
        max_length: int = 280
    ) -> Dict[str, Any]:
        """
        Create an attractive X/Twitter post from input text.
        
        Args:
            text: The input text to transform into a post
            style: Writing style - "professional", "casual", "witty", "inspirational"
            include_hashtags: Whether to include relevant hashtags
            max_length: Maximum character length (default 280)
            
        Returns:
            Dictionary with post text and metadata
        """
        try:
            # Generate the post based on style
            post_text = self._generate_post_text(text, style, include_hashtags, max_length)
            
            # Calculate statistics
            stats = {
                "character_count": len(post_text),
                "hashtag_count": len(re.findall(r'#\w+', post_text)),
                "emoji_count": len(re.findall(r'[\U0001F300-\U0001F9FF]', post_text)),
                "url_count": len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', post_text))
            }
            
            return {
                "success": True,
                "post_text": post_text,
                "stats": stats,
                "style": style,
                "ready_to_publish": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create post: {str(e)}"
            }
    
    def _generate_post_text(
        self,
        text: str,
        style: str,
        include_hashtags: bool,
        max_length: int
    ) -> str:
        """
        Generate post text based on input and style.
        Uses LLM API if available, falls back to simple formatting.
        """
        # Try to use LLM API for better results
        if self._has_anthropic or self._has_openai:
            try:
                return self._generate_with_llm(text, style, include_hashtags, max_length)
            except Exception as e:
                # Fall back to simple method if LLM fails
                print(f"LLM generation failed, using simple method: {str(e)}")
        
        # Fallback: simple method
        return self._generate_simple(text, style, include_hashtags, max_length)
    
    def _generate_with_llm(
        self,
        text: str,
        style: str,
        include_hashtags: bool,
        max_length: int
    ) -> str:
        """Generate post using LLM API (OpenAI or Anthropic)."""
        
        # Create the prompt
        prompt = self._build_llm_prompt(text, style, include_hashtags, max_length)
        
        # Try Anthropic first (Claude is generally better at creative writing)
        if self._has_anthropic:
            try:
                return self._generate_with_anthropic(prompt, max_length)
            except Exception as e:
                if not self._has_openai:
                    raise e
                # Fall through to OpenAI
        
        # Try OpenAI
        if self._has_openai:
            return self._generate_with_openai(prompt, max_length)
        
        raise Exception("No LLM API available")
    
    def _build_llm_prompt(
        self,
        text: str,
        style: str,
        include_hashtags: bool,
        max_length: int
    ) -> str:
        """Build the prompt for LLM post generation."""
        
        style_descriptions = {
            "professional": "professional, polished, and business-focused. Use appropriate business language and maintain credibility.",
            "casual": "friendly, conversational, and approachable. Use a relaxed tone like talking to a friend.",
            "witty": "clever, humorous, and entertaining. Be creative and add personality.",
            "inspirational": "motivational, uplifting, and encouraging. Inspire and energize the reader."
        }
        
        style_desc = style_descriptions.get(style, "engaging and authentic")
        
        hashtag_instruction = ""
        if include_hashtags:
            hashtag_instruction = "\n- Add 2-3 relevant hashtags at the end (on a new line)"
        
        prompt = f"""Transform the following text into an attractive X/Twitter post.

INPUT TEXT:
{text}

REQUIREMENTS:
- Style: {style_desc}
- Maximum length: {max_length} characters (strict limit!)
- Make it engaging and likely to get interaction
- Use emojis strategically to add visual appeal (1-2 relevant emojis)
- Keep it concise and punchy
- Ensure perfect grammar and spelling{hashtag_instruction}

OUTPUT ONLY THE POST TEXT, nothing else. No quotes, no explanations."""

        return prompt
    
    def _generate_with_anthropic(self, prompt: str, max_length: int) -> str:
        """Generate post using Anthropic Claude API."""
        if self._anthropic_client is None:
            try:
                from anthropic import Anthropic
                self._anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
        
        response = self._anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        post_text = response.content[0].text.strip()
        
        # Remove quotes if the model added them
        if post_text.startswith('"') and post_text.endswith('"'):
            post_text = post_text[1:-1]
        if post_text.startswith("'") and post_text.endswith("'"):
            post_text = post_text[1:-1]
        
        # Ensure we don't exceed max length
        if len(post_text) > max_length:
            post_text = self._smart_truncate(post_text, max_length)
        
        return post_text
    
    def _generate_with_openai(self, prompt: str, max_length: int) -> str:
        """Generate post using OpenAI API."""
        if self._openai_client is None:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
        
        response = self._openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "system",
                "content": "You are an expert social media manager who creates engaging X/Twitter posts. You always follow character limits strictly and create compelling, authentic content."
            }, {
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=300
        )
        
        post_text = response.choices[0].message.content.strip()
        
        # Remove quotes if the model added them
        if post_text.startswith('"') and post_text.endswith('"'):
            post_text = post_text[1:-1]
        if post_text.startswith("'") and post_text.endswith("'"):
            post_text = post_text[1:-1]
        
        # Ensure we don't exceed max length
        if len(post_text) > max_length:
            post_text = self._smart_truncate(post_text, max_length)
        
        return post_text
    
    def _generate_simple(
        self,
        text: str,
        style: str,
        include_hashtags: bool,
        max_length: int
    ) -> str:
        """
        Simple post generation without LLM (fallback method).
        """
        # Clean and truncate initial text
        cleaned_text = text.strip()
        
        # Style-specific formatting
        formatted_text = self._apply_style(cleaned_text, style)
        
        # Add hashtags if requested
        if include_hashtags:
            hashtags = self._extract_hashtags(cleaned_text, style)
            if hashtags and len(formatted_text) + len(hashtags) + 2 <= max_length:
                formatted_text = f"{formatted_text}\n\n{hashtags}"
        
        # Ensure we don't exceed max length
        if len(formatted_text) > max_length:
            # Truncate smartly (try to preserve complete words)
            formatted_text = self._smart_truncate(formatted_text, max_length)
        
        return formatted_text
    
    def _apply_style(self, text: str, style: str) -> str:
        """Apply style-specific formatting to text."""
        
        style_emojis = {
            "professional": "💼",
            "casual": "✨",
            "witty": "😄",
            "inspirational": "🚀"
        }
        
        style_prefixes = {
            "professional": "",
            "casual": "Hey! ",
            "witty": "",
            "inspirational": "✨ "
        }
        
        emoji = style_emojis.get(style, "")
        prefix = style_prefixes.get(style, "")
        
        # For inspirational style, add emoji at start
        if style == "inspirational" and not text.startswith(emoji):
            return f"{prefix}{text} {emoji}"
        elif style == "professional":
            return f"{prefix}{text} {emoji}"
        elif style == "witty":
            return f"{prefix}{text} {emoji}"
        else:
            return f"{prefix}{text}"
    
    def _extract_hashtags(self, text: str, style: str) -> str:
        """Extract or generate relevant hashtags."""
        # Simple hashtag extraction/generation
        # In production, use NLP or LLM to generate better hashtags
        
        common_hashtags = {
            "professional": ["#Business", "#Innovation", "#Leadership"],
            "casual": ["#Life", "#Daily", "#Thoughts"],
            "witty": ["#Humor", "#Fun", "#LOL"],
            "inspirational": ["#Motivation", "#Success", "#Growth"]
        }
        
        # Check for keywords that might indicate topics
        keywords_to_hashtags = {
            "ai": "#AI",
            "artificial intelligence": "#ArtificialIntelligence",
            "tech": "#Tech",
            "technology": "#Technology",
            "business": "#Business",
            "startup": "#Startup",
            "product": "#Product",
            "launch": "#Launch",
            "innovation": "#Innovation",
            "marketing": "#Marketing",
            "development": "#Development",
            "coding": "#Coding",
            "design": "#Design"
        }
        
        text_lower = text.lower()
        found_hashtags = []
        
        # Extract hashtags based on keywords
        for keyword, hashtag in keywords_to_hashtags.items():
            if keyword in text_lower and hashtag not in found_hashtags:
                found_hashtags.append(hashtag)
                if len(found_hashtags) >= 2:
                    break
        
        # If no hashtags found, use style defaults
        if not found_hashtags:
            found_hashtags = common_hashtags.get(style, ["#Share"])[:2]
        
        return " ".join(found_hashtags[:3])
    
    def _smart_truncate(self, text: str, max_length: int) -> str:
        """Truncate text smartly, preserving word boundaries."""
        if len(text) <= max_length:
            return text
        
        # Leave room for ellipsis
        truncate_length = max_length - 3
        
        # Try to truncate at word boundary
        truncated = text[:truncate_length]
        last_space = truncated.rfind(' ')
        
        if last_space > truncate_length * 0.8:  # If we have a reasonable word boundary
            return truncated[:last_space] + "..."
        else:
            return truncated + "..."
    
    def publish_post(self, post_text: str, confirm: bool = False) -> Dict[str, Any]:
        """
        Publish a post to X/Twitter.
        
        Args:
            post_text: The text to publish
            confirm: Must be True to actually publish (safety check)
            
        Returns:
            Dictionary with publish status and post URL if successful
        """
        if not confirm:
            return {
                "success": False,
                "error": "Publish confirmation required. Set confirm=True to publish.",
                "requires_confirmation": True
            }

        # Dry-run mode short-circuits real publishing but confirms the call path
        if self.dry_run:
            return {
                "success": True,
                "dry_run": True,
                "tweet_id": "dry-run",
                "tweet_url": "",
                "message": "Dry-run mode enabled (X_PUBLISH_DRY_RUN=true). No tweet was sent, but publish_post was called.",
                "post_text_echo": post_text
            }
        
        try:
            # Initialize Twitter client if needed
            if self._twitter_client is None:
                self._initialize_twitter_client()
            
            # Check if credentials are configured
            if not self._has_twitter_credentials():
                return {
                    "success": False,
                    "error": "X/Twitter API credentials not configured. Please set up .env file with your API keys.",
                    "requires_setup": True
                }
            
            # Publish the post
            response = self._twitter_client.create_tweet(text=post_text)
            
            # Get the tweet ID and construct URL
            tweet_id = response.data['id']
            username = self._get_username()
            tweet_url = f"https://x.com/{username}/status/{tweet_id}"
            
            return {
                "success": True,
                "tweet_id": tweet_id,
                "tweet_url": tweet_url,
                "message": f"Successfully published post! View at: {tweet_url}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to publish post: {str(e)}",
                "details": "Check your X/Twitter API credentials and permissions."
            }
    
    def _has_twitter_credentials(self) -> bool:
        """Check if Twitter API credentials are configured."""
        required_vars = [
            "X_API_KEY",
            "X_API_SECRET",
            "X_ACCESS_TOKEN",
            "X_ACCESS_TOKEN_SECRET"
        ]
        return all(os.getenv(var) for var in required_vars)
    
    def _initialize_twitter_client(self):
        """Initialize the Twitter API client."""
        try:
            import tweepy
            
            api_key = os.getenv("X_API_KEY")
            api_secret = os.getenv("X_API_SECRET")
            access_token = os.getenv("X_ACCESS_TOKEN")
            access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
            
            # Create client
            self._twitter_client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            
        except ImportError:
            raise ImportError("tweepy is not installed. Run: pip install tweepy")
        except Exception as e:
            raise Exception(f"Failed to initialize Twitter client: {str(e)}")
    
    def _get_username(self) -> str:
        """Get the authenticated user's username."""
        try:
            user = self._twitter_client.get_me()
            return user.data.username
        except:
            return "user"  # Fallback
