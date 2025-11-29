# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from database import engine, Base
# Import routers
from routers import auth, posts, comments, images, users

# --- Lifespan event for startup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Application startup...")
    async with engine.begin() as conn:
        # This creates the tables if they don't exist
        # ideally use Alembic for migrations, but this works for Hackathons
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables created/verified.")
    yield
    logging.info("Application shutdown...")

app = FastAPI(
    lifespan=lifespan,
    title="Community Task App",
    version="2.0"
)

# --- CORS ---
origins = ["*"] # Allow all for mobile app development

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Routers ---
app.include_router(auth.router, prefix="/api/auth")
app.include_router(users.router, prefix="/api")    # New Profile/Leaderboard logic
app.include_router(posts.router, prefix="/api")    # New Feed/Task logic
app.include_router(comments.router, prefix="/api/comments")
app.include_router(images.router, prefix="/api/images") # Keep existing image upload

@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "Community App API is running"}