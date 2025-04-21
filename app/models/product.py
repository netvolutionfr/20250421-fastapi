from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models import Base


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"
