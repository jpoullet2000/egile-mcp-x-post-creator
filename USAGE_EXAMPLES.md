# Usage Examples

## Basic Usage

### Creating Posts

#### Professional Style

```python
from egile_mcp_x_post_creator import server

# Create a professional business post
result = server.create_post(
    text="We're excited to announce our Q1 results with 150% revenue growth!",
    style="professional",
    include_hashtags=True
)
```

Output:
```
We're excited to announce our Q1 results with 150% revenue growth! 💼

#Business #Growth
```

#### Casual Style

```python
result = server.create_post(
    text="Just finished an amazing coding session. Feeling productive!",
    style="casual",
    include_hashtags=True
)
```

Output:
```
Hey! Just finished an amazing coding session. Feeling productive!

#Coding #Development
```

#### Witty Style

```python
result = server.create_post(
    text="Debugging: Being a detective in a crime movie where you're also the murderer",
    style="witty",
    include_hashtags=False
)
```

#### Inspirational Style

```python
result = server.create_post(
    text="Start where you are. Use what you have. Do what you can.",
    style="inspirational",
    include_hashtags=True
)
```

Output:
```
✨ Start where you are. Use what you have. Do what you can. 🚀

#Motivation #Success
```

### Publishing Posts

**Important:** Publishing requires explicit confirmation to prevent accidents.

```python
# Create a post first
post_text = "🚀 Just launched our new AI-powered feature! #AI #Innovation"

# Publish with confirmation
result = server.publish_post(
    post_text=post_text,
    confirm=True  # Must be True to actually publish
)
```

## Advanced Usage

### Custom Character Limits

```python
# Create a shorter post (for thread tweets)
result = server.create_post(
    text="This is the first tweet in a thread about AI development...",
    style="professional",
    max_length=200
)
```

### Without Hashtags

```python
# Create a post without hashtags
result = server.create_post(
    text="Clean, simple message without hashtags",
    style="casual",
    include_hashtags=False
)
```

## Integration Examples

### With Egile Agent Core

```python
from egile_agent_core import Agent, AgentConfig
from egile_agent_core.plugins.mcp_plugin import MCPPlugin

# Create an agent
config = AgentConfig(
    name="Social Media Manager",
    instructions="""
    You are a social media manager who helps create and publish 
    engaging X/Twitter posts. Always ask for confirmation before 
    publishing anything.
    """
)

agent = Agent(config)

# Add the MCP plugin
agent.add_plugin(MCPPlugin(
    server_script_path="path/to/egile-mcp-x-post-creator/src/egile_mcp_x_post_creator/server.py"
))

# Use the agent
response = agent.run(
    "Create an inspirational post about perseverance in software development"
)
```

### As a Standalone MCP Server

Run the server and connect it to Claude Desktop or other MCP clients:

```bash
# Run with stdio transport (for Claude Desktop)
python -m egile_mcp_x_post_creator

# Run with SSE transport (for web apps)
python -m egile_mcp_x_post_creator --transport sse --port 8000
```

### Testing Without Publishing

```python
from egile_mcp_x_post_creator.x_service import XPostService

service = XPostService()

# Create multiple posts
posts = []
topics = [
    "AI innovation",
    "Product launch",
    "Team achievement"
]

for topic in topics:
    result = service.create_post(
        text=f"Exciting news about {topic}!",
        style="professional"
    )
    if result['success']:
        posts.append(result['post_text'])

# Review all posts before publishing
for i, post in enumerate(posts, 1):
    print(f"Post {i}: {post}\n")
```

## Common Patterns

### Multi-Post Thread Creator

```python
# Create a thread of related posts
thread_topics = [
    "Introducing our new feature",
    "Here's how it works",
    "The benefits for users",
    "Try it today"
]

thread = []
for i, topic in enumerate(thread_topics, 1):
    result = service.create_post(
        text=f"{i}/{len(thread_topics)} {topic}",
        style="professional",
        max_length=240  # Leave room for thread numbering
    )
    if result['success']:
        thread.append(result['post_text'])
```

### Automated Posting with Approval

```python
def create_and_approve_post(text, style="professional"):
    """Create a post and ask for user approval before publishing."""
    
    # Create the post
    result = service.create_post(text=text, style=style)
    
    if not result['success']:
        print(f"Error creating post: {result['error']}")
        return
    
    # Show the post
    print(f"Generated post:\n{result['post_text']}\n")
    print(f"Stats: {result['stats']}\n")
    
    # Ask for confirmation
    confirm = input("Publish this post? (yes/no): ").lower() == 'yes'
    
    if confirm:
        publish_result = service.publish_post(
            post_text=result['post_text'],
            confirm=True
        )
        
        if publish_result['success']:
            print(f"Published! View at: {publish_result['tweet_url']}")
        else:
            print(f"Publish failed: {publish_result['error']}")
    else:
        print("Post not published.")

# Usage
create_and_approve_post("Just shipped a major update!", "casual")
```

### Scheduled Post Queue

```python
from datetime import datetime

class PostQueue:
    def __init__(self):
        self.queue = []
    
    def add_post(self, text, style="professional", scheduled_time=None):
        """Add a post to the queue."""
        result = service.create_post(text=text, style=style)
        
        if result['success']:
            self.queue.append({
                'text': result['post_text'],
                'scheduled': scheduled_time or datetime.now(),
                'published': False
            })
    
    def publish_due_posts(self):
        """Publish posts that are due."""
        now = datetime.now()
        
        for post in self.queue:
            if not post['published'] and post['scheduled'] <= now:
                # In real app, add confirmation flow here
                result = service.publish_post(
                    post_text=post['text'],
                    confirm=True
                )
                post['published'] = result['success']
```

## Error Handling

```python
def safe_post_creation(text, **kwargs):
    """Create a post with comprehensive error handling."""
    try:
        result = service.create_post(text=text, **kwargs)
        
        if not result['success']:
            print(f"Error: {result.get('error', 'Unknown error')}")
            return None
        
        # Validate post length
        if result['stats']['character_count'] > 280:
            print("Warning: Post exceeds 280 characters")
        
        return result['post_text']
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None
```

## Best Practices

1. **Always Review Before Publishing**: Never publish without reviewing the generated content
2. **Use Confirmation**: Always set `confirm=True` explicitly when publishing
3. **Test First**: Use `create_post` to preview before `publish_post`
4. **Handle Errors**: Check the `success` field in results
5. **Respect Rate Limits**: X/Twitter has rate limits for posting
6. **Keep Credentials Secure**: Never commit `.env` to version control
