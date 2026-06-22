"""
Chatbot router with local Ollama integration
"""
import httpx
import time
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models import Activity, ChatHistory
from app.routers.auth import get_current_user
from app.schemas import ChatMessage, ChatResponse, ChatHistoryResponse

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])


async def get_user_context(user_id: str, db: AsyncSession) -> str:
    """Get user context for chatbot prompt"""
    # Get recent activities
    query = select(Activity).where(Activity.user_id == user_id).limit(5)
    result = await db.execute(query)
    recent_activities = result.scalars().all()

    activities_summary = "\n".join(
        [
            f"- {a.activity_type}: {a.value} {a.unit} ({a.carbon_emissions} kg CO2)"
            for a in recent_activities
        ]
    )

    context = f"""User's recent activities:
{activities_summary}

You are an AI Carbon Footprint Coach. Help the user:
1. Understand their carbon emissions
2. Reduce their environmental impact
3. Set and achieve sustainability goals
4. Learn about eco-friendly alternatives

Be encouraging, informative, and practical."""

    return context


async def call_ollama(prompt: str, model: str = settings.OLLAMA_MODEL) -> tuple[str, int]:
    """
    Call Ollama API for text generation

    Returns:
        (response_text, response_time_ms)
    """
    try:
        async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT) as client:
            start_time = time.time()

            response = await client.post(
                f"{settings.OLLAMA_API_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.7,
                    "top_p": 0.9,
                },
            )

            elapsed_ms = int((time.time() - start_time) * 1000)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Ollama service unavailable",
                )

            data = response.json()
            return data.get("response", ""), elapsed_ms

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Ollama request timed out",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ollama error: {str(e)}",
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_message: ChatMessage,
    session_id: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message to the AI chatbot

    Args:
        chat_message: User's message
        session_id: Optional session ID for conversation continuity

    Returns:
        ChatResponse with AI response
    """
    # Use provided session ID or create new one
    if not session_id:
        session_id = str(uuid4())

    # Get user context
    context = await get_user_context(current_user["user_id"], db)

    # Build prompt
    prompt = f"""{context}

User: {chat_message.message}
Assistant:"""

    # Call Ollama
    ai_response, response_time = await call_ollama(prompt)

    # Get message count for this session
    query = select(ChatHistory).where(ChatHistory.session_id == session_id)
    result = await db.execute(query)
    messages = result.scalars().all()
    message_index = len(messages) + 1

    # Save to database
    chat_record = ChatHistory(
        id=uuid4(),
        user_id=current_user["user_id"],
        session_id=session_id,
        message_index=message_index,
        user_message=chat_message.message,
        ai_response=ai_response.strip(),
        response_time_ms=response_time,
        ai_model=settings.OLLAMA_MODEL,
    )

    db.add(chat_record)
    await db.commit()
    await db.refresh(chat_record)

    return chat_record


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get chat history for a session"""
    query = (
        select(ChatHistory)
        .where(
            ChatHistory.session_id == session_id,
            ChatHistory.user_id == current_user["user_id"],
        )
        .order_by(ChatHistory.message_index)
    )

    result = await db.execute(query)
    messages = result.scalars().all()

    return ChatHistoryResponse(
        total_messages=len(messages),
        messages=messages,
    )


@router.delete("/history/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_chat_history(
    session_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Clear chat history for a session"""
    query = select(ChatHistory).where(
        ChatHistory.session_id == session_id,
        ChatHistory.user_id == current_user["user_id"],
    )

    result = await db.execute(query)
    messages = result.scalars().all()

    for message in messages:
        await db.delete(message)

    await db.commit()


@router.get("/status", response_model=dict)
async def check_ollama_status():
    """Check if Ollama is available"""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{settings.OLLAMA_API_URL}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return {
                    "status": "online",
                    "available_models": [m.get("name") for m in models],
                    "current_model": settings.OLLAMA_MODEL,
                }
    except Exception:
        pass

    return {
        "status": "offline",
        "message": "Ollama service is not available at " + settings.OLLAMA_API_URL,
    }
