import json
import requests

def test_chat_endpoint():
    # Test data
    test_request = {
        "message": "Hello"
    }
    print("hello")
    # Make request to chat endpoint
    response = requests.post("http://127.0.0.1:8000/chat/", json=test_request, stream=True)
    response.raise_for_status()
    
    for line in response.iter_lines():
        if line:
            # print("before decode: ", line)
            line = line.decode('utf-8')
            # print("after decode: ", line)
            if line.startswith('data: '):
                line = line[6:]  # Remove 'data: ' prefix
                if line.strip() == '[DONE]':
                    break
                try:
                    chunk = json.loads(line)
                    if chunk.get('content'):
                        yield chunk.get('content')
                except json.JSONDecodeError:
                    continue
    



try:
    content = ''
    print("Streaming response:")
    for token in test_chat_endpoint():
        content += token
    print("\nStream completed")
    print("content: ", content)
except Exception as e:
    print(f"Error: {e}")

