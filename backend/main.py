from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
from openai import OpenAI
from .settings import settings
from .search_engine import SearchEngine
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Compass API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine and OpenAI client
search_engine = SearchEngine()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class ChatRequest(BaseModel):
    """Chat request model."""
    message: str

class AdviceRequest(BaseModel):
    """Advice request model with snippets."""
    message: str
    snippets: List[Dict[str, Any]]

def build_prompt(message: str, snippets: List[Dict[str, Any]]) -> str:
    """Build GPT-4 prompt from message and snippets."""
    snippets_text = ""
    for i, snippet in enumerate(snippets, 1):
        snippets_text += f"Q{i}: {snippet['Context']}\nA{i}: {snippet['Response']}\n\n"
        
    return f"""You are Compass, an empathetic mental-health companion.
Never diagnose or prescribe.

User message: {message}

Here are 5 professional Q&A snippets to help inform your response:
{snippets_text}

Using these insights, write one supportive reply with practical coping steps.
If the user seems in crisis, first list the hotline.

At the end add: "{settings.DISCLAIMER}"
"""

@app.post("/api/chat")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    """Return relevant snippets for user message."""
    try:
        logger.info(f"Received chat request: {request.message}")
        
        # Check for crisis keywords
        is_crisis = search_engine.check_crisis(request.message)
        logger.info(f"Crisis check result: {is_crisis}")
        
        if is_crisis:
            return {
                "crisis": True,
                "hotline": "988 Suicide & Crisis Lifeline - Call or text 988",
                "snippets": []
            }
            
        # Get relevant snippets
        try:
            snippets = search_engine.search(request.message)
            logger.info(f"Found {len(snippets)} relevant snippets")
            return {
                "crisis": False,
                "snippets": snippets
            }
        except Exception as search_error:
            logger.error(f"Search error: {str(search_error)}")
            raise HTTPException(status_code=500, detail=f"Search error: {str(search_error)}")
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def stream_response(message: str) -> str:
    """Stream GPT-4's response."""
    stream = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "user", "content": message}],
        max_tokens=settings.MAX_TOKENS,
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content

@app.post("/api/get_advice")
async def get_advice(request: AdviceRequest) -> StreamingResponse:
    """Get personalized advice using GPT-4."""
    try:
        # Build prompt
        prompt = build_prompt(request.message, request.snippets)
        
        # Return streaming response
        return StreamingResponse(
            stream_response(prompt),
            media_type="text/event-stream"
        )
        
    except Exception as e:
        logger.error(f"Get advice error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 