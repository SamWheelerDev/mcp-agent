from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db, Recipe

router = APIRouter()


# Pydantic models for request/response
class RecipeBase(BaseModel):
    name: str
    description: str
    ingredients: str
    instructions: str
    prep_time: int
    cook_time: int
    image_url: Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class RecipeResponse(RecipeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RecipeListResponse(BaseModel):
    recipes: List[RecipeResponse]
    total: int


# Endpoints
@router.post("/recipes", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = Recipe(
        name=recipe.name,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        prep_time=recipe.prep_time,
        cook_time=recipe.cook_time,
        image_url=recipe.image_url,
    )

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe


@router.get("/recipes", response_model=RecipeListResponse)
def get_recipes(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Recipe)

    # Apply search filter if provided
    if search:
        query = query.filter(Recipe.name.ilike(f"%{search}%"))

    # Get total count
    total = query.count()

    # Apply pagination
    recipes = query.order_by(Recipe.name).offset(skip).limit(limit).all()

    return {"recipes": recipes, "total": total}


@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe


@router.put("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int, recipe_update: RecipeBase, db: Session = Depends(get_db)
):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    # Update recipe attributes
    for key, value in recipe_update.dict().items():
        setattr(db_recipe, key, value)

    db.commit()
    db.refresh(db_recipe)

    return db_recipe


@router.delete("/recipes/{recipe_id}", response_model=dict)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(db_recipe)
    db.commit()

    return {"message": "Recipe deleted successfully"}


# Sample recipes for initial data
SAMPLE_RECIPES = [
    {
        "name": "Overnight Oats with Berries",
        "description": "A healthy and easy breakfast option that you can prepare the night before.",
        "ingredients": "1/2 cup rolled oats, 1/2 cup milk, 1/4 cup Greek yogurt, 1 tbsp chia seeds, 1 tbsp honey, 1/4 cup mixed berries",
        "instructions": "1. Mix oats, milk, yogurt, chia seeds, and honey in a jar. 2. Cover and refrigerate overnight. 3. Top with berries before serving.",
        "prep_time": 5,
        "cook_time": 0,
        "image_url": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8b3Zlcm5pZ2h0JTIwb2F0c3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60",
    },
    {
        "name": "Chicken and Vegetable Stir-Fry",
        "description": "A quick and nutritious dinner option that's perfect for meal prep.",
        "ingredients": "2 chicken breasts, 1 bell pepper, 1 broccoli head, 2 carrots, 3 tbsp soy sauce, 1 tbsp honey, 2 cloves garlic, 1 tbsp ginger, 2 tbsp olive oil",
        "instructions": "1. Cut chicken and vegetables into bite-sized pieces. 2. Heat oil in a wok or large pan. 3. Cook chicken until no longer pink. 4. Add vegetables and stir-fry for 5 minutes. 5. Mix soy sauce, honey, minced garlic, and ginger, then add to the pan. 6. Cook for another 2-3 minutes until sauce thickens.",
        "prep_time": 15,
        "cook_time": 15,
        "image_url": "https://images.unsplash.com/photo-1512058564366-18510be2db19?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8c3RpcmZyeXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60",
    },
    {
        "name": "Mediterranean Quinoa Salad",
        "description": "A refreshing and protein-packed salad that keeps well for several days.",
        "ingredients": "1 cup quinoa, 1 cucumber, 1 cup cherry tomatoes, 1/2 red onion, 1/2 cup feta cheese, 1/4 cup kalamata olives, 2 tbsp olive oil, 1 lemon, 1 tsp dried oregano, salt and pepper to taste",
        "instructions": "1. Cook quinoa according to package instructions and let cool. 2. Dice cucumber, halve tomatoes, and finely chop red onion. 3. Mix quinoa with vegetables, crumbled feta, and olives. 4. Whisk together olive oil, lemon juice, oregano, salt, and pepper. 5. Pour dressing over salad and toss to combine.",
        "prep_time": 15,
        "cook_time": 20,
        "image_url": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8cXVpbm9hJTIwc2FsYWR8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60",
    },
]


# Function to seed sample recipes
def seed_sample_recipes(db: Session):
    # Check if recipes already exist
    if db.query(Recipe).count() > 0:
        return

    # Add sample recipes
    for recipe_data in SAMPLE_RECIPES:
        db_recipe = Recipe(**recipe_data)
        db.add(db_recipe)

    db.commit()
