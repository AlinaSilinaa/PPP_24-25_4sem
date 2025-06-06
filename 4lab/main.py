from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Base
from database import engine, SessionLocal
from schemas import Store, StoreCreate, Product, ProductCreate
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/stores", response_model=List[Store])
def read_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_stores(db, skip=skip, limit=limit)

@app.post("/stores", response_model=Store, status_code=201)
def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    return crud.create_store(db, store)

@app.put("/stores/{store_id}", response_model=Store)
def update_store(store_id: int, store: StoreCreate, db: Session = Depends(get_db)):
    return crud.update_store(db, store_id, store)

@app.get("/stores/{store_id}/products", response_model=List[Product])
def read_store_products(store_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, store_id=store_id, skip=skip, limit=limit)

@app.get("/products", response_model=List[Product])
def read_products(store_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, store_id=store_id, skip=skip, limit=limit)

@app.post("/products", response_model=Product, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, product_id)