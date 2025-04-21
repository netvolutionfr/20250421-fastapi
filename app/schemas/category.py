from __future__ import annotations

from .base import SchemaBase


class CategoryCreate(SchemaBase):
    name: str
    description: str | None = None

class CategoryUpdate(SchemaBase):
    name: str | None = None
    description: str | None = None

class CategoryLite(SchemaBase):
    id: int
    name: str
    description: str | None = None

class CategoryResponse(CategoryLite):
    products: list[ProductLite] = []
