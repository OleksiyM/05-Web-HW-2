# https://gemini.google.com/ Google Gemini AI tool was used for generating code

from fastapi import FastAPI, APIRouter, Body, Path, Query, HTTPException, status, Depends, templates
from fastapi_oauth2_auth import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from jinja2 import TemplateResponse

# Database configuration
engine = create_engine("postgresql://username:password@host:port/database")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Template directory
templates = templates.TemplateDirectory(template_dir="templates")

# Main app
app = FastAPI()

# Item data model
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None

# Items router
items_router = APIRouter(prefix="/items")

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create item
@items_router.post("/", dependencies=[Depends(get_db)])
async def create_item(item: Item, db: SessionLocal = Depends(get_db)):
    # Implement actual item creation logic using SQLAlchemy
    # ...
    db.add(item)
    db.commit()
    return {"message": f"Item created with ID: {item.id}"}

# Get all items
@items_router.get("/", dependencies=[Depends(get_db)])
async def get_all_items(db: SessionLocal = Depends(get_db)):
    # Implement actual item retrieval logic using SQLAlchemy
    # ...
    items = db.query(Item).all()
    return items

# Get item by ID
@items_router.get("/{item_id}", dependencies=[Depends(get_db)])
async def get_item_by_id(item_id: int = Path(..., description="The ID of the item to retrieve"), db: SessionLocal = Depends(get_db)):
    # Implement actual item retrieval logic using SQLAlchemy
    # ...
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# Update item
@items_router.put("/{item_id}", dependencies=[Depends(get_db)])
async def update_item(item_id: int = Path(..., description="The ID of the item to update"),
                      new_data: Item = Body(..., description="New data for the item"), db: SessionLocal = Depends(get_db)):
    # Implement actual item update logic using SQLAlchemy
    # ...
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    for field, value in new_data.dict().items():
        setattr(item, field, value)
    db.commit()
    return {"message": f"Item {item_id} updated successfully"}

# Delete item
@items_router.delete("/{item_id}", dependencies=[Depends(get_db)])
async def delete_item(item_id: int = Path(..., description="The ID of the item to delete"), db: SessionLocal = Depends(get_db)):
    # Implement actual item deletion logic using SQLAlchemy
    # ...
    item = db.query(Item).get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} deleted successfully"}

# Add router to app
app.include_router(items_router)

# Authentication endpoints
@app.post("/login")
async def login(username: str = Body(...), password: str = Body(...)):
    # Simulate authentication with actual user database or service
    if username == "admin" and password == "secret":
        access_token = "fake_oauth2_token"  # Replace with actual token generation
        return {"access_token": access_token}
    else:
        raise HTTP

# https://copilot.microsoft.com/ Microsoft Copilot AI tool was used for generating code


# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import APIRouter

# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/database"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

# Pydantic schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# FastAPI application
app = FastAPI()

# Initialize templates
templates = Jinja2Templates(directory="templates")

# For hashing the password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# To get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

items_router = APIRouter()

@items_router.post("/")
def create_item(item: ItemCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return create_item(db=db, item=item)

@items_router.get("/")
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    items = get_items(db, skip=skip, limit=limit)
    return items

@items_router.get("/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    item = get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@items_router.put("/{item_id}")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return update_item(db=db, item_id=item_id, item=item)

@items_router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    delete_item(db=db, item_id=item_id)
    return {"detail": "Item deleted"}

app.include_router(items_router, prefix="/items")

