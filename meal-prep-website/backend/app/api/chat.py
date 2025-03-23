from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
import anthropic

from ..database import get_db, ChatHistory, User
from ..config import settings

router = APIRouter()


# Pydantic models for request/response
class ChatMessageCreate(BaseModel):
    user_id: int
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    user_id: int
    message: str
    response: str
    timestamp: datetime

    class Config:
        orm_mode = True


class ChatHistoryResponse(BaseModel):
    messages: List[ChatMessageResponse]


# Anthropic client
client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


# Helper function to generate response from Anthropic Claude
async def generate_response(message: str) -> str:
    try:
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": message}],
            system="""You are a meal prep and cooking assistant with access to recipe databases 
            and nutrition information. Your job is to help users plan their meals for the week based on 
            their preferences, dietary restrictions, and ingredients they have available.
            
            Follow this conversation flow:
            1. Ask about dietary preferences and restrictions
            2. Inquire about ingredients they currently have
            3. Discuss their meal prep goals (number of meals, variety preferences)
            4. Suggest appropriate recipes and meal plans
            5. Provide cooking tips and substitutions when needed
            
            Be friendly, helpful, and provide detailed information about recipes including 
            ingredients, preparation steps, nutrition facts, and cooking times.""",
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I'm having trouble processing your request right now. Please try again later."


# Endpoints
@router.post("/chat", response_model=ChatMessageResponse)
async def create_chat_message(
    chat_message: ChatMessageCreate, db: Session = Depends(get_db)
):
    # Check if user exists
    user = db.query(User).filter(User.id == chat_message.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate response from Claude
    response_text = await generate_response(chat_message.message)

    # Create chat history entry
    db_chat = ChatHistory(
        user_id=chat_message.user_id,
        message=chat_message.message,
        response=response_text,
    )

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return db_chat


@router.get("/chat/history/{user_id}", response_model=ChatHistoryResponse)
def get_chat_history(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get chat history
    messages = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user_id)
        .order_by(ChatHistory.timestamp.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {"messages": messages}
