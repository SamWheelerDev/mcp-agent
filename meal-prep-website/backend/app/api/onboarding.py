"""
Onboarding API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from ..database import get_db
from ..agents import OnboardingAgent

router = APIRouter()


# Request and response models
class OnboardingStepData(BaseModel):
    step_id: str
    data: Dict[str, Any]


class OnboardingResponse(BaseModel):
    status: str
    message: Optional[str] = None
    current_step: Optional[Dict[str, Any]] = None
    total_steps: Optional[int] = None
    progress: Optional[float] = None
    profile: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None


# Initialize the onboarding agent
onboarding_agent = None


async def get_agent():
    """Get or initialize the onboarding agent."""
    global onboarding_agent
    if onboarding_agent is None:
        onboarding_agent = OnboardingAgent()
        await onboarding_agent.initialize()
    return onboarding_agent


@router.post("/start", response_model=OnboardingResponse)
async def start_onboarding(
    user_id: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    agent: OnboardingAgent = Depends(get_agent),
):
    """
    Start the onboarding process for a user.
    """
    try:
        result = await agent.start_onboarding(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/step", response_model=OnboardingResponse)
async def process_step(
    user_id: str = Body(...),
    step_data: OnboardingStepData = Body(...),
    db: Session = Depends(get_db),
    agent: OnboardingAgent = Depends(get_agent),
):
    """
    Process an onboarding step.
    """
    try:
        result = await agent.process_step(user_id, step_data.step_id, step_data.data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current-step/{user_id}", response_model=OnboardingResponse)
async def get_current_step(
    user_id: str,
    db: Session = Depends(get_db),
    agent: OnboardingAgent = Depends(get_agent),
):
    """
    Get the current onboarding step for a user.
    """
    try:
        result = await agent.get_current_step(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete", response_model=OnboardingResponse)
async def complete_onboarding(
    user_id: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    agent: OnboardingAgent = Depends(get_agent),
):
    """
    Complete the onboarding process for a user.
    """
    try:
        result = await agent.complete_onboarding(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preferences/{user_id}", response_model=OnboardingResponse)
async def get_user_preferences(
    user_id: str,
    db: Session = Depends(get_db),
    agent: OnboardingAgent = Depends(get_agent),
):
    """
    Get the preferences for a user.
    """
    try:
        result = await agent.get_user_preferences(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
