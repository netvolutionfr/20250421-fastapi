from app.schemas.category import CategoryResponse, CategoryLite
from app.schemas.product import ProductResponse, ProductLite

ProductResponse.model_rebuild()
CategoryResponse.model_rebuild()
CategoryLite.model_rebuild()
ProductLite.model_rebuild()
