from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Product, User, Category
from app.routes.auth import get_current_user
from app.schemas.product import ProductResponse, ProductLite, ProductCreate, ProductUpdate

router = APIRouter(tags=["products"])

@router.get("/products/", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.category))  # Load related category
    )
    return result.scalars().all()

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.category))  # Load related category
        .where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    if product is None:
        return {"message": "Product not found"}
    return product

@router.post("/products/", response_model=ProductLite)
async def create_product(
        product_in: ProductCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    product = Product(**product_in.model_dump())
    if product.category_id:
        # Vérifier que la catégorie existe (facultatif mais conseillé)
        result = await db.execute(select(Category).where(Category.id == product.category_id))
        category = result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=400, detail="Catégorie non trouvée")
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
        product_id: int, updates: ProductUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Product)
        .options(selectinload(Product.category))  # Load related category
        .where(Product.id == product_id)
    )
    product = result.scalars().first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = updates.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category_id = update_data["category_id"]
        if category_id is not None:
            result = await db.execute(select(Category).where(Category.id == category_id))
            category = result.scalar_one_or_none()
            if not category:
                raise HTTPException(status_code=400, detail="Catégorie non trouvée")

        setattr(product, "category_id", category_id)
        del update_data["category_id"]

    for key, value in update_data.items():
        setattr(product, key, value)

    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/products/{product_id}")
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return {"message": "Product deleted"}
