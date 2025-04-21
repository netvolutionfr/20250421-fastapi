from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.models import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)

    products = relationship('Product', back_populates='category')

    def __repr__(self):
        return f"<Category(name={self.name})>"

