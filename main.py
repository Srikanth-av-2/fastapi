from fastapi import FastAPI, Depends
from models import Products
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

products = [
    Products(id=1, name="Laptop", price=999.99, description="A high-performance laptop", quantity=56),
    Products(id=2, name="Smartphone", price=499.99, description="A powerful smartphone with a great camera", quantity=39),
    Products(id=3, name="Headphones", price=199.99, description="Noise-cancelling over-ear headphones", quantity=78),
    Products(id=4, name="Smartwatch", price=299.99, description="A stylish smartwatch with fitness tracking features", quantity=83)
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Products).count
    if not count:
        for product in products:
            db.add(database_models.Products(**product.model_dump()))

        db.commit()

init_db()

@app.get("/")
def greet():
    return "Hello, World!"

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Products).all()
    return db_products

@app.get("/product/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id==id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/product")
def add_product(product: Products, db: Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return product

@app.put("/product")
def update_product(product_id: int, updated_product: Products, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id==product_id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return "Product updated"
    return {"error": "Product not found"}


@app.delete("/product")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id==product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    return {"error": "Product not found"}
