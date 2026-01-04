# LLM Integration Guide

## Overview

The X Post Creator uses LLM APIs (Large Language Models) to generate natural, engaging posts. This results in much better content than simple template-based generation.

## Supported LLMs

1. **Anthropic Claude** (Recommended)
   - Model: Claude Sonnet 3.5
   - Best for creative and nuanced writing
   - Excellent at matching tone and style

2. **OpenAI GPT**
   - Model: GPT-4o
   - Strong alternative option
   - Great at following instructions

## Selection Priority

The service automatically selects the best available LLM:

1. **Anthropic Claude** (tried first if API key present)
2. **OpenAI GPT** (tried if Anthropic unavailable)
3. **Simple Generation** (fallback if no API keys)

## Setup

### Option 1: Anthropic Claude (Recommended)

1. Create an account at [console.anthropic.com](https://console.anthropic.com)
2. Generate an API key
3. Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

### Option 2: OpenAI GPT

1. Create an account at [platform.openai.com](https://platform.openai.com)
2. Generate an API key
3. Add to `.env`:
   ```bash
   OPENAI_API_KEY=sk-proj-...
   ```

### Option 3: Both (Best reliability)

Add both keys to `.env` for maximum reliability and automatic fallback:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
```

## How It Works

### LLM Prompt Engineering

For each post, the service creates a sophisticated prompt that includes:

- **Input text**: Your original content
- **Style requirements**: Professional, casual, witty, or inspirational
- **Character limits**: Strict 280 character limit
- **Formatting instructions**: Emoji usage, hashtag placement
- **Quality guidelines**: Engagement optimization, grammar rules

### Example LLM Prompt

```
Transform the following text into an attractive X/Twitter post.

INPUT TEXT:
Just launched our new AI-powered analytics dashboard

REQUIREMENTS:
- Style: professional, polished, and business-focused
- Maximum length: 280 characters (strict limit!)
- Make it engaging and likely to get interaction
- Use emojis strategically (1-2 relevant emojis)
- Add 2-3 relevant hashtags at the end

OUTPUT ONLY THE POST TEXT, nothing else.
```

### LLM Response Processing

The service:
1. Sends the prompt to the LLM
2. Receives the generated post
3. Cleans up formatting (removes quotes, extra spaces)
4. Validates character count
5. Truncates intelligently if needed

## Comparison: LLM vs Simple Generation

### Input
```
"We just shipped a major performance update to our platform"
```

### LLM-Generated (Claude)
```
🚀 Big news! We just shipped a major performance update 
to our platform.

Faster load times. Smoother experience. Better for everyone.

#ProductUpdate #Performance #UserExperience
```

### Simple Generation
```
We just shipped a major performance update to our platform 💼

#Business #Innovation
```

## Cost Considerations

### Anthropic Claude
- **Model**: claude-3-5-sonnet-20241022
- **Cost**: ~$0.003 per post (300 tokens)
- **Free tier**: $5 credit for new accounts

### OpenAI GPT
- **Model**: gpt-4o
- **Cost**: ~$0.002 per post (300 tokens)
- **Free tier**: $5 credit for new accounts

**Note**: Costs are minimal - you can generate thousands of posts for a few dollars.

## Benefits of Using LLM

1. **Natural Language**: Posts sound authentic and human
2. **Context Understanding**: LLM understands your intent
3. **Tone Matching**: Perfect style adaptation
4. **Creative Enhancement**: Adds compelling hooks and formatting
5. **Hashtag Intelligence**: Generates relevant, trending hashtags
6. **Emoji Selection**: Strategic emoji placement for engagement

## Fallback Behavior

If LLM generation fails or no API key is configured:

```python
# Service automatically falls back to simple generation
service = XPostService()

# This works even without API keys
result = service.create_post(
    text="Your text here",
    style="professional"
)
# Uses template-based generation instead
```

## Testing LLM Integration

Run the LLM example to see the difference:

```bash
python example_with_llm.py
```

This will show you:
- LLM-generated posts for different styles
- Comparison between LLM and simple generation
- Statistics and metadata

## Best Practices

1. **Use LLM for important posts**: Product launches, announcements
2. **Simple generation for routine posts**: If cost is a concern
3. **Review LLM output**: Always check before publishing
4. **Experiment with styles**: Try different styles to find your voice
5. **Monitor costs**: Set up billing alerts in your LLM provider dashboard

## Troubleshooting

### LLM not being used

Check:
1. API key is correctly set in `.env`
2. API key is valid and has credits
3. Check console for error messages
4. Verify packages are installed: `pip install anthropic openai`

### Posts too long

The service automatically truncates, but you can:
1. Use shorter input text
2. Set a lower `max_length` parameter
3. Adjust the style (some styles are more verbose)

### Rate limits

If you hit rate limits:
1. Add delays between requests
2. Use multiple API keys (rotate)
3. Implement caching for similar requests

## Advanced: Custom LLM Configuration

You can modify the LLM behavior in [x_service.py](src/egile_mcp_x_post_creator/x_service.py):

- Change the model (e.g., use GPT-4-turbo)
- Adjust temperature for more/less creativity
- Modify the system prompt
- Add custom instructions

Example:
```python
# In _generate_with_anthropic method
response = self._anthropic_client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=300,
    temperature=0.9,  # More creative (default: 0.7)
    messages=[...]
)
```
