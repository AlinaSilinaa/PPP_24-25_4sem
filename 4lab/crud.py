from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Store, Product
from schemas import StoreCreate, ProductCreate

def get_store(db: Session, store_id: int):
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()

def create_store(db: Session, store: StoreCreate):
    db_store = Store(**store.dict())
    db.add(db_store)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Store already exists")
    db.refresh(db_store)
    return db_store

def update_store(db: Session, store_id: int, store: StoreCreate):
    db_store = get_store(db, store_id)
    for field, value in store.dict().items():
        setattr(db_store, field, value)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Store already exists")
    db.refresh(db_store)
    return db_store

def get_products(db: Session, store_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(Product)
    if store_id is not None:
        query = query.filter(Product.store_id == store_id)
    return query.offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    if not db.query(Store).filter(Store.id == product.store_id).first():
        raise HTTPException(status_code=404, detail="Store not found")
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()