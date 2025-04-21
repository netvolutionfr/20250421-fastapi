from __future__ import annotations

from .base import SchemaBase


class ProductCreate(SchemaBase):
    name: str
    description: str | None = None
    price: float
    stock: int
    category_id: int | None = None

class ProductUpdate(SchemaBase):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    category_id: int | None = None

class ProductLite(SchemaBase):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int
    category_id: int | None = None

class ProductResponse(ProductLite):
    category: CategoryLite | None = None
