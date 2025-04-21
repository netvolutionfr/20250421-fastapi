from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Category, User
from app.routes.auth import get_current_user
from app.schemas.category import CategoryResponse, CategoryLite, CategoryCreate

router = APIRouter(tags=["categories"])

@router.get("/categories/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category)
        .options(selectinload(Category.products))  # Load related products
    )
    return result.scalars().all()

@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Category)
        .options(selectinload(Category.products))  # Load related products
        .where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()
    if category is None:
        return {"message": "Category not found"}
    return category

@router.post("/categories/", response_model=CategoryLite)
async def create_category(
        category_in: CategoryCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    category = Category(**category_in.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category
