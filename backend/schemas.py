# backend/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import TaskStatus # Import the enum we defined

# --- Token (Login) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- User ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    points: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Comment ---
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime
    author: Optional[User] = None # Nested user info

    class Config:
        from_attributes = True

# --- Like ---
class Like(BaseModel):
    user_id: int
    post_id: int
    class Config:
        from_attributes = True

# --- Post (The Main Task) ---
class PostBase(BaseModel):
    image_url: str
    image_public_id: str
    caption: Optional[str] = None
    latitude: float
    longitude: float

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    status: TaskStatus # open, pending, completed
    proof_image_url: Optional[str] = None
    
    created_at: datetime
    author_id: int
    resolved_by_id: Optional[int] = None
    
    author: Optional[User] = None
    resolved_by: Optional[User] = None # Show who fixed it
    comments: List[Comment] = []
    likes: List[Like] = []

    class Config:
        from_attributes = True