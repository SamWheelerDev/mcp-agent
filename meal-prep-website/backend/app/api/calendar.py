from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime, timedelta

from ..database import get_db, MealPlan, Recipe, User
from ..config import settings

router = APIRouter()


# Pydantic models for request/response
class MealPlanBase(BaseModel):
    user_id: int
    plan_date: date
    meal_type: str
    recipe_id: int


class MealPlanCreate(MealPlanBase):
    pass


class MealPlanResponse(MealPlanBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class MealPlanWithRecipe(MealPlanResponse):
    recipe_name: str
    recipe_description: str

    class Config:
        orm_mode = True


class MealPlanListResponse(BaseModel):
    meal_plans: List[MealPlanWithRecipe]


# Endpoints
@router.post("/meal-plans", response_model=MealPlanResponse)
def create_meal_plan(meal_plan: MealPlanCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == meal_plan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if recipe exists
    recipe = db.query(Recipe).filter(Recipe.id == meal_plan.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Check if meal plan already exists for this date and meal type
    existing_plan = (
        db.query(MealPlan)
        .filter(
            MealPlan.user_id == meal_plan.user_id,
            MealPlan.plan_date == meal_plan.plan_date,
            MealPlan.meal_type == meal_plan.meal_type,
        )
        .first()
    )

    if existing_plan:
        # Update existing plan
        existing_plan.recipe_id = meal_plan.recipe_id
        db.commit()
        db.refresh(existing_plan)
        return existing_plan

    # Create new meal plan
    db_meal_plan = MealPlan(
        user_id=meal_plan.user_id,
        plan_date=meal_plan.plan_date,
        meal_type=meal_plan.meal_type,
        recipe_id=meal_plan.recipe_id,
    )

    db.add(db_meal_plan)
    db.commit()
    db.refresh(db_meal_plan)

    return db_meal_plan


@router.get("/meal-plans", response_model=MealPlanListResponse)
def get_meal_plans(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Set default date range to current week if not provided
    if not start_date:
        today = date.today()
        start_date = today - timedelta(days=today.weekday())  # Monday of current week

    if not end_date:
        end_date = start_date + timedelta(days=6)  # Sunday of current week

    # Query meal plans with recipe information
    meal_plans_with_recipes = (
        db.query(
            MealPlan,
            Recipe.name.label("recipe_name"),
            Recipe.description.label("recipe_description"),
        )
        .join(Recipe, MealPlan.recipe_id == Recipe.id)
        .filter(
            MealPlan.user_id == user_id,
            MealPlan.plan_date >= start_date,
            MealPlan.plan_date <= end_date,
        )
        .order_by(MealPlan.plan_date, MealPlan.meal_type)
        .all()
    )

    # Convert to response model
    result = []
    for mp, recipe_name, recipe_description in meal_plans_with_recipes:
        meal_plan_dict = {
            "id": mp.id,
            "user_id": mp.user_id,
            "plan_date": mp.plan_date,
            "meal_type": mp.meal_type,
            "recipe_id": mp.recipe_id,
            "created_at": mp.created_at,
            "recipe_name": recipe_name,
            "recipe_description": recipe_description,
        }
        result.append(meal_plan_dict)

    return {"meal_plans": result}


@router.delete("/meal-plans/{meal_plan_id}", response_model=dict)
def delete_meal_plan(meal_plan_id: int, db: Session = Depends(get_db)):
    db_meal_plan = db.query(MealPlan).filter(MealPlan.id == meal_plan_id).first()
    if not db_meal_plan:
        raise HTTPException(status_code=404, detail="Meal plan not found")

    db.delete(db_meal_plan)
    db.commit()

    return {"message": "Meal plan deleted successfully"}


# Helper function to generate a weekly meal plan
@router.post("/generate-weekly-plan", response_model=MealPlanListResponse)
async def generate_weekly_plan(
    user_id: int, start_date: Optional[date] = None, db: Session = Depends(get_db)
):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Set default start date to next Monday if not provided
    if not start_date:
        today = date.today()
        days_until_monday = (7 - today.weekday()) % 7
        start_date = today + timedelta(days=days_until_monday)

    # Get all recipes
    recipes = db.query(Recipe).all()
    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")

    # Create a simple meal plan for the week
    meal_types = ["breakfast", "lunch", "dinner"]
    meal_plans = []

    # Generate a 7-day meal plan
    for day_offset in range(7):
        current_date = start_date + timedelta(days=day_offset)

        for meal_type in meal_types:
            # Select a random recipe for each meal
            import random

            recipe = random.choice(recipes)

            # Check if meal plan already exists
            existing_plan = (
                db.query(MealPlan)
                .filter(
                    MealPlan.user_id == user_id,
                    MealPlan.plan_date == current_date,
                    MealPlan.meal_type == meal_type,
                )
                .first()
            )

            if existing_plan:
                # Update existing plan
                existing_plan.recipe_id = recipe.id
                db.commit()
                db.refresh(existing_plan)
                meal_plan = existing_plan
            else:
                # Create new meal plan
                meal_plan = MealPlan(
                    user_id=user_id,
                    plan_date=current_date,
                    meal_type=meal_type,
                    recipe_id=recipe.id,
                )
                db.add(meal_plan)
                db.commit()
                db.refresh(meal_plan)

            # Add to result
            meal_plans.append(
                {
                    "id": meal_plan.id,
                    "user_id": meal_plan.user_id,
                    "plan_date": meal_plan.plan_date,
                    "meal_type": meal_plan.meal_type,
                    "recipe_id": meal_plan.recipe_id,
                    "created_at": meal_plan.created_at,
                    "recipe_name": recipe.name,
                    "recipe_description": recipe.description,
                }
            )

    return {"meal_plans": meal_plans}
