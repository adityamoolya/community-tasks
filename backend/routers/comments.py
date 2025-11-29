# routers/comment.py

from fastapi import APIRouter, Depends, HTTPException
# --- MODIFIED: Import AsyncSession for type hinting ---
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import schemas, crud
from database import get_db
from auth_utils import get_current_active_user

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

# --- MODIFIED: Path and parameter changed to post_id ---
@router.get("/post/{post_id}", response_model=List[schemas.Comment])
async def get_comments_for_post(post_id: int, db: AsyncSession = Depends(get_db)):
    # --- MODIFIED: Awaited the async crud function and updated its name ---
    return await crud.get_comments_by_post(db, post_id=post_id)

# --- MODIFIED: Function is now async ---
@router.post("/", response_model=schemas.Comment)
async def create_comment(
    comment: schemas.CommentCreate,
    # --- MODIFIED: Parameter changed to post_id ---
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    # --- MODIFIED: Awaited the async crud function ---
    db_post = await crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # --- MODIFIED: Awaited the async crud function and updated parameter name ---
    return await crud.create_comment(db=db, comment_data=comment, author_id=current_user.id, post_id=post_id)

# --- MODIFIED: Function is now async ---
@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    # --- MODIFIED: Awaited the async crud function ---
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user is comment author or admin
    if db_comment.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # --- MODIFIED: Awaited the async crud function ---
    await crud.delete_comment(db=db, comment_id=comment_id)
    return {"message": "Comment deleted successfully"}