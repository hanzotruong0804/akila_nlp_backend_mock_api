import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import tiktoken

mock_content = """
### Device Information Table

| Device ID | Device Name       | Device Type | Description                                |
|-----------|-------------------|-------------|--------------------------------------------|
| 001       | Temperature Sensor| Sensor      | Measures ambient temperature               |
| 002       | Smart Light       | Light       | Adjustable brightness and color            |
| 003       | Security Camera   | Camera      | HD video recording with night vision       |

### Chart block example

```chart
{
  "chart_name": "the equipment abc energy consumption",
  "args": {
    "equipment_id": "UK-bcd-ZvbBxnkupfHPIRy56zSf72Wm",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }
}
```

feel free to ask more!
"""
enc = tiktoken.get_encoding("o200k_base")

router = APIRouter(prefix="/chat", tags=["Chat"])

async def generate_mock_response_stream(user_message: str):
    """
    Stream message back similar to ChatGPT without using llm.
    """
    for token in enc.encode(user_message):
      data = {"content": enc.decode([token])}
      print(f"chunk: {json.dumps(data)}")
      yield f"data: {json.dumps(data)}\n\n"
        # await asyncio.sleep(0.01)  # Reduce transmission latency


@router.post("/")
async def chat(request: dict):
    """
    API Chat streaming SSE.
    """
    return StreamingResponse(generate_mock_response_stream(mock_content), media_type="text/event-stream")

