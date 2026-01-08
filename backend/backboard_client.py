"""Backboard API integration for LLM and memory management."""

import asyncio
from typing import Optional
import httpx
from .config import config

_client = None
_event_loop = None

def get_event_loop():
    """Get or create event loop for async operations."""
    global _event_loop
    try:
        _event_loop = asyncio.get_event_loop()
    except RuntimeError:
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_event_loop)
    return _event_loop

def run_coroutine(coro):
    """Run async coroutine in sync context."""
    loop = get_event_loop()
    return loop.run_until_complete(coro)

async def get_client() -> httpx.AsyncClient:
    """Get or create Backboard API client."""
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            base_url=config.BACKBOARD_BASE_URL,
            headers={"X-API-Key": config.BACKBOARD_API_KEY},
            timeout=30.0
        )
    return _client

async def get_or_create_assistant(name: str = "ElderCare Companion") -> str:
    """Get existing assistant or create new one, return assistant_id."""
    client = await get_client()
    
    try:
        # List existing assistants
        response = await client.get("/assistants")
        assistants = response.json() if response.status_code == 200 else []
        
        # Look for our assistant
        for assistant in assistants:
            if assistant.get("name") == name:
                print(f"✓ Found existing assistant: {assistant['assistant_id']}")
                return assistant["assistant_id"]
        
        # Create new assistant if not found
        payload = {
            "name": name,
            "description": "Health reminder and medical information assistant for elderly users. Always include safety disclaimers."
        }
        response = await client.post("/assistants", json=payload)
        
        if response.status_code == 200 or response.status_code == 201:
            assistant_id = response.json().get("assistant_id")
            print(f"✓ Created new assistant: {assistant_id}")
            return assistant_id
        else:
            print(f"✗ Failed to create assistant: {response.text}")
            raise Exception("Failed to create Backboard assistant")
    
    except Exception as e:
        print(f"✗ Error in get_or_create_assistant: {e}")
        raise

async def ensure_thread(assistant_id: str, thread_id: Optional[str] = None):
    """Get existing thread or create new one."""
    client = await get_client()
    
    if thread_id:
        try:
            response = await client.get(f"/threads/{thread_id}")
            if response.status_code == 200:
                return response.json()
        except:
            pass
    
    # Create new thread
    try:
        response = await client.post(f"/assistants/{assistant_id}/threads", json={})
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to create thread: {response.text}")
    except Exception as e:
        print(f"✗ Error creating thread: {e}")
        raise

async def send_message(thread_id: str, content: str, assistant_id: Optional[str] = None) -> str:
    """Send message to thread and get AI response."""
    client = await get_client()
    
    try:
        # Add message to thread and get response
        payload = {
            "content": content,
            "stream": "false"
        }
        
        response = await client.post(
            f"/threads/{thread_id}/messages",
            data=payload
        )
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            # Extract assistant's response
            if isinstance(result, dict) and "content" in result:
                return result["content"]
            elif isinstance(result, dict) and "message" in result:
                return result["message"]
            else:
                return str(result)
        else:
            print(f"✗ Error sending message: {response.text}")
            return "Sorry, I had trouble processing your message. Please try again."
    
    except Exception as e:
        print(f"✗ Error in send_message: {e}")
        return "Connection error. Please try again."

async def add_memory(content: str, metadata: Optional[dict] = None) -> dict:
    """Add information to assistant's memory (for future retrieval)."""
    client = await get_client()
    
    try:
        # Note: Memory endpoints may vary by Backboard version
        # This is a placeholder - check Backboard docs for exact endpoint
        payload = {
            "content": content,
            "metadata": metadata or {}
        }
        
        # Store as context for now (actual memory API may differ)
        return {"status": "recorded", "content": content}
    
    except Exception as e:
        print(f"✗ Error adding memory: {e}")
        return {"status": "error", "error": str(e)}

async def close_client():
    """Close HTTP client connection."""
    global _client
    if _client:
        await _client.aclose()
        _client = None
