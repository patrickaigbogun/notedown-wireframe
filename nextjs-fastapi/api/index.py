# Standard library imports
import re
import uuid
import os
from dotenv import load_dotenv
import bcrypt
from datetime import datetime
from typing import Optional, List

# FastAPI and related imports
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Database and model imports
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

# Authentication
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

# Pydantic models for request/response validation
from pydantic import BaseModel, EmailStr, Field

# Local application imports
from database.models import User, UserActivity, Note
from database.main import get_db
from uuid import UUID

# Load environment variables
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


security = HTTPBearer()

# Initialize FastAPI application
app = FastAPI(
    title="NoteDown API",
    description="FastAPI-powered backend service for secure note management",
    version="1.0.0",
    openapi_tags=[
        {"name": "Authentication", "description": "User registration and login operations"},
        {"name": "User Management", "description": "User activity and account management"},
        {"name": "Notes", "description": "Note CRUD operations"}
    ]
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input validation models
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    is_private: bool = False

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str]
    is_private: Optional[bool] = None

class NoteResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    is_private: bool
    created_at: datetime

class DeleteNoteRequest(BaseModel):
    user_id: UUID

# Utility functions
def hash_password_with_id(password: str, user_id: str) -> str:
    combined = f"{password}{user_id}"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(combined.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password_with_id(plain_password: str, user_id: str, hashed_password: str) -> bool:
    combined = f"{plain_password}{user_id}"
    return bcrypt.checkpw(combined.encode("utf-8"), hashed_password.encode("utf-8"))

def check_route_exists(app: FastAPI, request: Request) -> bool:
    for route in app.routes:
        if isinstance(route, APIRoute):
            if re.fullmatch(route.path, request.url.path):
                if request.method in route.methods:
                    return True
    return False

def decode_user_token(token: str, username: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token,
            f"{JWT_SECRET}{username}",
            algorithms=[JWT_ALGORITHM]  
        )
        return payload.get("user_id")
    except (ExpiredSignatureError, InvalidTokenError):
        return None

# Authentication Routes
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        user_id = str(uuid.uuid4())
        hashed_password = hash_password_with_id(user.password, user_id)

        new_user = User(
            id=user_id,
            username=user.username,
            email=user.email,
            password=hashed_password,
        )
        db.add(new_user)
        db.add(UserActivity(user_id=user_id))
        db.commit()

        return {
            "message": f"User '{user.username}' registered successfully",
            "userid": user_id
        }
    except IntegrityError as e:
        db.rollback()
        if isinstance(e.orig, UniqueViolation):
            if "username" in str(e.orig):
                raise HTTPException(status_code=400, detail="Username already in use.")
            if "email" in str(e.orig):
                raise HTTPException(status_code=400, detail="Email already registered.")
        raise HTTPException(status_code=400, detail="Database integrity error occurred.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Registration error: {str(e)}")

@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password required.")

    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and verify_password_with_id(
        user.password, str(db_user.id), db_user.password
    ):
        token = jwt.encode(
            {"user_id": str(db_user.id)},
            f"{JWT_SECRET}{user.username}",
            algorithm=JWT_ALGORITHM
        )
        return {
            "message": f"Login successful! Welcome back, {user.username}",
            "userid": str(db_user.id),
            "token": token
        }
    raise HTTPException(status_code=400, detail="Invalid credentials.")

# User Activity Routes
@app.get("/get_user_activity/{username}", tags=["User Management"])
async def get_activity(
    username: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    user_id = decode_user_token(token, username)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token. Please login again."
        )

    try:
        user_id_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    activity = db.query(UserActivity).filter(
        UserActivity.user_id == user_id_uuid
    ).first()

    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    return {
        "notes_created": activity.notes_created,
        "notes_deleted": activity.notes_deleted,
        "notes_shared": activity.notes_shared,
        "times_logged_in": activity.times_logged_in,
        "private_notes": activity.private_notes
    }

@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(user)
        db.commit()
        return {"message": f"User '{user_id}' and all associated data deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

# Note Management Routes
@app.post("/create_note/{user_id}", response_model=NoteResponse)
async def create_note(user_id: uuid.UUID, note: NoteCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User ID '{user_id}' not found.")

    try:
        new_note = Note(
            id=uuid.uuid4(),
            user_id=user_id,
            title=note.title,
            content=note.content,
            is_private=note.is_private,
            created_at=datetime.utcnow(),
        )
        db.add(new_note)

        activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).first()
        activity.notes_created += 1
        if note.is_private:
            activity.private_notes += 1

        db.commit()
        db.refresh(new_note)

        return NoteResponse(
            id=new_note.id,
            title=new_note.title,
            content=new_note.content,
            is_private=new_note.is_private,
            created_at=new_note.created_at,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Note creation failed: {str(e)}")

@app.get("/get_notes/{user_id}", response_model=List[NoteResponse])
async def get_notes(user_id: uuid.UUID, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    if not notes:
        return []
    return notes

@app.put("/update_note/{note_id}")
async def update_note(note_id: UUID, note_update: NoteUpdate, user_id: UUID, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or unauthorized.")

    if note_update.title is not None:
        note.title = note_update.title
    if note_update.content is not None:
        note.content = note_update.content
    if note_update.is_private is not None:
        note.is_private = note_update.is_private

    try:
        db.commit()
        return {"message": f"Note '{note_id}' updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Update failed: {str(e)}")

@app.delete("/delete_note/{note_id}")
async def delete_note(note_id: UUID, delete_request: DeleteNoteRequest, db: Session = Depends(get_db)):
    user_id = delete_request.user_id
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User ID '{user_id}' not found.")

    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found or unauthorized.")

    try:
        activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).first()

        db.delete(note)
        db.commit()
        return {"message": f"Note '{note_id}' deleted successfully."}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Failed to delete the note due to database integrity issue.",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

# Catch-All Route
@app.api_route(
    "/{path_name:path}",
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"],
    include_in_schema=False
)
async def catch_all(request: Request, path_name: str):
    if not check_route_exists(app, request):
        return JSONResponse(
            status_code=404,
            content={"detail": f"404 - Requested resource '{path_name}' not found."},
        )
    raise HTTPException(status_code=404)

# Custom Exception Handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404, content={"detail": "Custom 404 - Resource not found"}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )