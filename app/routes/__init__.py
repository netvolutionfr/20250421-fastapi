from .products import router as products_router
from .categories import router as categories_router
from .auth import router as auth_router

__all__ = [
    "products_router",
    "categories_router",
    "auth_router"
]
