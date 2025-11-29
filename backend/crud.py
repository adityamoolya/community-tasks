# crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import or_
import cloudinary.uploader

import models, schemas
from auth_utils import get_password_hash

# --- User CRUD ---
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- Post CRUD ---
async def get_posts(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 10, 
    album: str = None, 
    tag: str = None,
    search: str = None
):
    query = select(models.Post).options(
        selectinload(models.Post.tags), 
        selectinload(models.Post.album),
        selectinload(models.Post.author),
        selectinload(models.Post.comments)
    )
    
    if album:
        query = query.join(models.Album).filter(models.Album.name == album)
    if tag:
        query = query.join(models.Post.tags).filter(models.Tag.name == tag)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Post.title.ilike(search_term),
                models.Post.caption.ilike(search_term),
                models.Post.alt_text.ilike(search_term)
            )
        )
    
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(models.Post)
        .options(
            selectinload(models.Post.comments), 
            selectinload(models.Post.tags),
            selectinload(models.Post.author),
            selectinload(models.Post.album)
        )
        .filter(models.Post.id == post_id)
    )
    return result.scalars().first()

async def create_post(db: AsyncSession, post: schemas.PostCreate, author_id: int):
    tag_objects = []
    for tag_name in post.tags:
        result = await db.execute(select(models.Tag).filter(models.Tag.name == tag_name))
        tag = result.scalars().first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            await db.commit()
        tag_objects.append(tag)
    
    db_post = models.Post(**post.model_dump(exclude={"tags"}), author_id=author_id)
    db_post.tags = tag_objects
    
    db.add(db_post)
    await db.commit()
    
    # This is the crucial line that prevents the error.
    # It re-fetches the post with all its relationships loaded.
    return await get_post(db, post_id=db_post.id)

async def update_post(db: AsyncSession, post_id: int, post_data: schemas.PostCreate):
    db_post = await get_post(db, post_id)
    if db_post:
        update_data = post_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_post, key, value)
        await db.commit()
        await db.refresh(db_post)
    return db_post

async def delete_post(db: AsyncSession, post_id: int):
    db_post = await get_post(db, post_id)
    if db_post:
        if db_post.image_public_id:
            try:
                cloudinary.uploader.destroy(db_post.image_public_id)
            except Exception as e:
                print(f"Failed to delete image from Cloudinary: {e}")

        await db.delete(db_post)
        await db.commit()
    return db_post

# --- Comment, Like, and Album CRUD (no changes needed) ---
async def get_comments_by_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(models.Comment).filter(models.Comment.post_id == post_id))
    return result.scalars().all()

async def get_comment(db: AsyncSession, comment_id: int):
    result = await db.execute(select(models.Comment).filter(models.Comment.id == comment_id))
    return result.scalars().first()

async def create_comment(db: AsyncSession, comment: schemas.CommentCreate, author_id: int, post_id: int):
    db_comment = models.Comment(**comment.model_dump(), author_id=author_id, post_id=post_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def delete_comment(db: AsyncSession, comment_id: int):
    db_comment = await get_comment(db, comment_id)
    if db_comment:
        await db.delete(db_comment)
        await db.commit()
    return db_comment

async def get_like(db: AsyncSession, user_id: int, post_id: int):
    result = await db.execute(
        select(models.Like).filter(models.Like.user_id == user_id, models.Like.post_id == post_id)
    )
    return result.scalars().first()

async def create_like(db: AsyncSession, user_id: int, post_id: int):
    db_like = models.Like(user_id=user_id, post_id=post_id)
    db.add(db_like)
    await db.commit()
    await db.refresh(db_like)
    return db_like

async def delete_like(db: AsyncSession, user_id: int, post_id: int):
    db_like = await get_like(db, user_id=user_id, post_id=post_id)
    if db_like:
        await db.delete(db_like)
        await db.commit()
    return db_like

async def get_albums(db: AsyncSession):
    result = await db.execute(select(models.Album))
    return result.scalars().all()

async def get_album_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(models.Album).filter(models.Album.name == name))
    return result.scalars().first()

async def create_album(db: AsyncSession, album: schemas.AlbumCreate):
    db_album = models.Album(**album.model_dump())
    db.add(db_album)
    await db.commit()
    await db.refresh(db_album)
    return db_album