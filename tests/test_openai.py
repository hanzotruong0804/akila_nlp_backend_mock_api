import requests
import os
from typing import List, Dict, Any, Generator
import json

from dotenv import load_dotenv
load_dotenv()


def call_openai_api_stream(messages: List[Dict[str, Any]], api_key: str = None) -> Generator[str, None, None]:
    """
    Call OpenAI API with streaming response.
    
    Args:
        messages: List of message dictionaries
        api_key: OpenAI API key. If None, will try to get from environment variable OPENAI_API_KEY
        
    Yields:
        Generated text tokens as they arrive
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not provided and not found in environment variables")

    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "gpt-4",
        "messages": messages,
        "response_format": {
            "type": "text"
        },
        "temperature": 1,
        "max_completion_tokens": 2048,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "store": False,
        "stream": True
    }
    
    response = requests.post(url, headers=headers, json=data, stream=True)
    response.raise_for_status()
    
    for line in response.iter_lines():
        if line:
            print("raw line before decode: ", line)
            line = line.decode('utf-8')
            print("raw line after decode: ", line)
            if line.startswith('data: '):
                line = line[6:]  # Remove 'data: ' prefix
                if line.strip() == '[DONE]':
                    break
                try:
                    chunk = json.loads(line)
                    if chunk.get('choices') and chunk['choices'][0].get('delta', {}).get('content'):
                        yield chunk['choices'][0]['delta']['content']
                except json.JSONDecodeError:
                    continue

# Example usage
if __name__ == "__main__":
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "tesst"
                }
            ]
        },
    ]
    

    try:
        print("Streaming response:")
        for token in call_openai_api_stream(messages):
            print(token, end='', flush=True)
        print("\nStream completed")
    except Exception as e:
        print(f"Error: {e}")
