# backend/routers/posts.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

import schemas, models
from database import get_db
from auth_utils import get_current_active_user
# Reuse your existing image uploader logic? 
# If difficult, just import the function directly or duplicate the logic briefly here.
from routers.images import upload_image # Assuming this function is reusable or available

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# --- 1. GET FEED (Only Open or Pending Tasks) ---
@router.get("/", response_model=List[schemas.Post])
async def get_feed(
    skip: int = 0, 
    limit: int = 20, 
    db: AsyncSession = Depends(get_db)
):
    # Show OPEN tasks (Red markers) and PENDING (Yellow markers - maybe to show activity)
    # Don't show COMPLETED (Green) in the main "work" feed.
    query = (
        select(models.Post)
        .where(models.Post.status != models.TaskStatus.COMPLETED)
        .order_by(desc(models.Post.created_at))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()

# --- 2. CREATE REQUEST ---
@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_request(
    post_data: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    new_post = models.Post(
        image_url=post_data.image_url,
        image_public_id=post_data.image_public_id,
        caption=post_data.caption,
        latitude=post_data.latitude,
        longitude=post_data.longitude,
        author_id=current_user.id,
        status=models.TaskStatus.OPEN # Starts as Open
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

# --- 3. VOLUNTEER SUBMITS PROOF (Step A) ---
# The Flutter app first uploads the image to /api/images/upload, gets the URL,
# then sends the URL here.
@router.post("/{post_id}/submit-proof")
async def submit_proof(
    post_id: int,
    proof_image_url: str, # Received from frontend
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Fetch post
    result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Task not found")

    if post.status != models.TaskStatus.OPEN:
        raise HTTPException(status_code=400, detail="Task is not open for contributions")
    
    if post.author_id == current_user.id:
         raise HTTPException(status_code=400, detail="You cannot claim your own task")

    # Update Post
    post.status = models.TaskStatus.PENDING_VERIFICATION
    post.resolved_by_id = current_user.id
    post.proof_image_url = proof_image_url
    
    await db.commit()
    return {"message": "Proof submitted! Waiting for author approval."}

# --- 4. AUTHOR APPROVES & CLOSES (Step B) ---
@router.post("/{post_id}/approve")
async def approve_and_close(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Fetch post with the volunteer relationship loaded
    # We need 'resolved_by' to add points to them
    query = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(query)
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Task not found")

    # Security: Only author can approve
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the author can approve this")

    if post.status != models.TaskStatus.PENDING_VERIFICATION:
        raise HTTPException(status_code=400, detail="No pending proof to approve")

    # AWARD POINTS TO VOLUNTEER
    # We need to fetch the volunteer user object
    volunteer_query = select(models.User).where(models.User.id == post.resolved_by_id)
    volunteer_result = await db.execute(volunteer_query)
    volunteer = volunteer_result.scalars().first()
    
    if volunteer:
        volunteer.points += 50 # Give them 50 points!
    
    # Close the task
    post.status = models.TaskStatus.COMPLETED
    
    await db.commit()
    return {"message": "Task approved! Points awarded to the volunteer."}