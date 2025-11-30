# 🌍 Community Task Force App (Backend)

A community-driven platform where people can report environmental issues (like garbage piles or areas needing cleanup) and volunteers can resolve them. Designed with **FastAPI**, **PostgreSQL**, and a **Flutter frontend**—built for speed, clarity, and real-world impact.

## 🚀 Features

### 🛡️ Core Capabilities
* **Report Issues:** Users create tasks with photos and GPS coordinates.
* **Map View:** All open tasks appear on a map, making it easy for volunteers to act.
* **Proof Workflow:**
    1. A volunteer completes the task and uploads proof.
    2. The task owner reviews the proof.
    3. Once approved, the task is marked *Closed*.
* **Gamified Rewards:** Verified contributions earn points, powering the global **Leaderboard**.

### ⚙️ Technical Highlights
* **FastAPI:** Async, high-performance Python backend.
* **PostgreSQL:** Stable, scalable relational storage.
* **Cloudinary:** Efficient image hosting and transformation.
* **Argon2:** Strong password hashing.
* **Eager Loading:** Prevents N+1 query issues for high-traffic scenarios.

---

## 📂 Project Structure

```text
backend/
├── main.py              # Entry point and router setup
├── database.py          # Async DB connection (PostgreSQL/SQLite) with SSL
├── models.py            # SQLAlchemy models (Users, Posts, Comments)
├── schemas.py           # Pydantic validation & response models
├── crud.py              # Database operations (Create/Read/Update)
├── auth_utils.py        # JWT generation, Argon2 hashing, OAuth2 flows
├── requirements.txt     # Python dependencies
├── Procfile             # Deployment config (Railway/Heroku)
└── routers/             # API modules by feature
    ├── auth.py          # Login & registration
    ├── posts.py         # Tasks, proofs, approval lifecycle
    ├── users.py         # Profiles, stats, leaderboard
    ├── comments.py      # Task discussions
    └── images.py        # Cloudinary upload wrapper
```

---

## 🛠️ Local Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in `backend/`:

```ini
# --- Database ---
# Local (SQLite)
DATABASE_URL=sqlite+aiosqlite:///./local_test.db
# Production (PostgreSQL)
# DATABASE_URL=postgresql+asyncpg://user:pass@host:port/dbname

# --- Security ---
SECRET_KEY=your_random_secret_key

# --- Cloudinary ---
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret

# --- Mock Mode ---
USE_MOCK_CLOUD=False
```

### 5. Run the Server

```bash
uvicorn main:app --reload
```

API lives at: **http://127.0.0.1:8000**

---

## 📖 API Documentation

FastAPI provides automatic interactive docs:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

### Core Endpoints

| Method | Endpoint | Description |
|-------|----------|-------------|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/token` | Login and receive JWT token |
| `GET` | `/api/posts/` | View all open tasks |
| `POST` | `/api/posts/` | Create a new task |
| `POST` | `/api/posts/{id}/submit-proof` | Volunteer submits cleanup proof |
| `POST` | `/api/posts/{id}/approve` | Owner approves and closes task |
| `GET` | `/api/users/leaderboard` | View top contributors |

---

## ☁️ Deployment (Railway)

1. Connect GitHub repo to Railway.  
2. Add a **PostgreSQL** service.  
3. Add the backend service.  
4. Set `DATABASE_URL` from the Postgres service.  
5. Add all `CLOUDINARY_*` variables and `SECRET_KEY`.  
6. Railway deploys automatically using the `Procfile`.

---

