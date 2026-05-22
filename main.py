from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import Products
from database import session, engine
import database_models
from sqlalchemy.orm import Session
from sqlalchemy import select

app = FastAPI()

#database_models.Base.metadata.create_all(bind=engine)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(
            database_models.Base.metadata.create_all
        )

products = [
    Products(id=1, name="Laptop", price=999.99, description="A high-performance laptop", quantity=56),
    Products(id=2, name="Smartphone", price=499.99, description="A powerful smartphone with a great camera", quantity=39),
    Products(id=3, name="Headphones", price=199.99, description="Noise-cancelling over-ear headphones", quantity=78),
    Products(id=4, name="Smartwatch", price=299.99, description="A stylish smartwatch with fitness tracking features", quantity=83)
]
'''
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
'''
async def get_db():
    async with session() as db:
        yield db


async def init_db():

    async with session() as db:

        result = await db.execute(
            select(database_models.Products)
        )

        products_in_db = result.scalars().all()

        if not products_in_db:

            for product in products:
                db.add(
                    database_models.Products(
                        **product.model_dump()
                    )
                )

            await db.commit()

@app.on_event("startup")
async def startup():
    await create_tables()
    await init_db()

@app.get("/")
def greet():
    return "Hello, World!"

@app.get("/products")
async def get_products(db: AsyncSession = Depends(get_db)):
         #db_products = db.query(database_models.Products).all()

         result = await db.execute(select(database_models.Products))
         db_products = result.scalars().all()
         return db_products

@app.get("/product/{id}")
async def get_product(id: int, db: AsyncSession = Depends(get_db)):
        #db_product = db.query(database_models.Products).filter(database_models.Products.id==id).first()

        result = await db.execute(select(database_models.Products).where(database_models.Products.id==id))
        db_product = result.scalar()
        if db_product:
            return db_product
        return "product not found"

@app.post("/product")
async def add_product(product: Products, db: AsyncSession = Depends(get_db)):
        db.add(database_models.Products(**product.model_dump()))
        
        await db.commit()
        return product

@app.put("/product")
async def update_product(product_id: int, updated_product: Products, db: AsyncSession = Depends(get_db)):
        #db_product = db.query(database_models.Products).filter(database_models.Products.id==product_id).first()

        result = await db.execute(select(database_models.Products).where(database_models.Products.id == product_id))
        db_product = result.scalar()
        if db_product:
            db_product.name = updated_product.name
            db_product.description = updated_product.description
            db_product.price = updated_product.price
            db_product.quantity = updated_product.quantity
            await db.commit()
            return "Product updated"
        return {"error": "Product not found"}


@app.delete("/product")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    #db_product = db.query(database_models.Products).filter(database_models.Products.id==product_id).first()

    result = await db.execute(select(database_models.Products).where(database_models.Products.id == product_id))
    db_product = result.scalar()
    if db_product:
        await db.delete(db_product)
        await db.commit()
        return "Product deleted"
    return {"error": "Product not found"}
