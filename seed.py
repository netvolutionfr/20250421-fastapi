from app.database import engine, AsyncSessionLocal
from app.models import Base, User, Product, Category
from app.auth import hash_password
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def run_seed():

    async with AsyncSessionLocal() as session:

        users = [
            User(username="stanis", email="stanis@example.com", hashed_password=hash_password("123456")),
        ]

        categories = [
            Category(name="Informatique", description="Ordinateurs et accessoires"),
            Category(name="Livres", description="Romans et manuels"),
            Category(name="Vêtements", description="Mode et accessoires"),
            Category(name="Électronique", description="Téléphones et gadgets"),
        ]

        session.add_all(users + categories)
        await session.flush()

        result = await session.execute(select(Category))
        cats = {c.name: c.id for c in result.scalars()}
        products = [
            # Informatique
            Product(name="PC Lenovo", description="16Go RAM", price=899.99, stock=10, category_id=cats["Informatique"]),
            Product(name="PC HP", description="8Go RAM", price=699.99, stock=5, category_id=cats["Informatique"]),
            Product(name="PC ASUS", description="32Go RAM", price=1299.99, stock=3, category_id=cats["Informatique"]),
            Product(name="MacBook Pro", description="16Go RAM, 512Go SSD", price=1999.99, stock=2, category_id=cats["Informatique"]),

            # Électronique
            Product(name="iPhone 16", description="128Go", price=999.99, stock=20, category_id=cats["Électronique"]),
            Product(name="iPad Pro", description="256Go", price=1099.99, stock=8, category_id=cats["Électronique"]),
            Product(name="Samsung Galaxy S21", description="256Go", price=899.99, stock=15, category_id=cats["Électronique"]),


            # Livres
            Product(name="Le Petit Prince", description="Un classique de la littérature", price=9.99, stock=50, category_id=cats["Livres"]),
            Product(name="Harry Potter à l'école des sorciers", description="Le premier tome de la saga", price=19.99, stock=30, category_id=cats["Livres"]),
            Product(name="Le Seigneur des Anneaux", description="Une épopée fantastique", price=29.99, stock=20, category_id=cats["Livres"]),
            Product(name="1984", description="Roman dystopique de George Orwell", price=14.99, stock=25, category_id=cats["Livres"]),

            # Vêtements
            Product(name="T-shirt Noir", description="T-shirt en coton noir", price=19.99, stock=100, category_id=cats["Vêtements"]),
            Product(name="Jean Bleu", description="Jean slim fit", price=49.99, stock=50, category_id=cats["Vêtements"]),
            Product(name="Veste en Cuir", description="Veste en cuir véritable", price=99.99, stock=20, category_id=cats["Vêtements"]),
            Product(name="Robe Rouge", description="Robe d'été rouge", price=39.99, stock=30, category_id=cats["Vêtements"]),
        ]

        session.add_all(products)
        await session.commit()

    print("✅ Seed terminé.")

async def main():
    await init_db()
    await run_seed()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
