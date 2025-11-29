# database.py

import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# --- ADDED: Load environment variables from a .env file ---
load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    logger.critical("DATABASE_URL not found in environment variables.")
    raise ValueError("No DATABASE_URL found. Please set it in your .env file.")

# --- MODIFIED: Switched to create_async_engine for async support ---
engine = create_async_engine(DATABASE_URL)

# --- MODIFIED: Configured sessionmaker for async sessions ---
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# --- MODIFIED: get_db is now an async function ---
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()