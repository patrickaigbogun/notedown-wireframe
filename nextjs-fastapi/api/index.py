# Standard library imports
import re
import uuid
import bcrypt
from datetime import datetime
from typing import Optional

# FastAPI and related imports
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Database and model imports
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

# Pydantic models for request/response validation
from pydantic import BaseModel, EmailStr, Field

# Local application imports
from database.models import User, UserActivity, Note
from database.main import get_db

# Initialize FastAPI application
app = FastAPI()

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
    """Model for user registration data validation."""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    """Model for user login data validation."""
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

class NoteCreate(BaseModel):
    """Model for note creation data validation."""
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    is_private: bool = False

class NoteResponse(BaseModel):
    """Model for note response data."""
    id: uuid.UUID
    title: str
    content: str
    is_private: bool
    created_at: datetime

def hash_password_with_id(password: str, user_id: str) -> str:
    """
    Hash a password using bcrypt with the user's ID as additional salt.
    
    Args:
        password: Plain text password
        user_id: User's unique identifier
    Returns:
        Hashed password as string
    """
    combined = f"{password}{user_id}"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(combined.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password_with_id(plain_password: str, user_id: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash using the user's ID.
    
    Args:
        plain_password: Password to verify
        user_id: User's unique identifier
        hashed_password: Stored hashed password
    Returns:
        Boolean indicating if password matches
    """
    combined = f"{plain_password}{user_id}"
    return bcrypt.checkpw(combined.encode('utf-8'), hashed_password.encode('utf-8'))

def check_route_exists(app: FastAPI, request: Request) -> bool:
    """
    Check if a route exists for the given path and HTTP method.
    
    Args:
        app: FastAPI application instance
        request: Incoming HTTP request
    Returns:
        Boolean indicating if route exists
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            if re.fullmatch(route.path, request.url.path):
                if request.method in route.methods:
                    return True
    return False

# Route handlers
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
async def catch_all(request: Request, path_name: str):
    """Catch-all route handler for undefined endpoints."""
    if not check_route_exists(app, request):
        return JSONResponse(
            status_code=404,
            content={"detail": f"404 - Requested resource '{path_name}' not found."}
        )
    return None

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    """
    Handle user registration.
    Creates new user record and associated activity tracking.
    """
    try:
        user_id = str(uuid.uuid4())
        hashed_password = hash_password_with_id(user.password, user_id)

        new_user = User(
            id=user_id,
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        db.add(new_user)
        db.add(UserActivity(user_id=user_id))
        db.commit()

        return {"message": f"User '{user.username}' registered successfully. Your user ID is {user_id}."}
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
    """Handle user login with username and password verification."""
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Username and password required.")
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and verify_password_with_id(user.password, str(db_user.id), db_user.password):
        return {"message": f"Login successful! Welcome back, {user.username}."}
    raise HTTPException(status_code=400, detail="Invalid credentials.")

@app.post("/create_note/{user_id}", response_model=NoteResponse)
async def create_note(user_id: uuid.UUID, note: NoteCreate, db: Session = Depends(get_db)):
    """
    Create a new note for a user and update their activity metrics.
    """
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
            created_at=datetime.utcnow()
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
            created_at=new_note.created_at
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Note creation failed: {str(e)}")

@app.delete("/delete_note/{note_id}")
async def delete_note(note_id: uuid.UUID, user_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Delete a note and update user activity metrics.
    Verifies note ownership before deletion.
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User ID '{user_id}' not found.")
    
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note not found or unauthorized.")
    
    try:
        activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).first()
        activity.notes_deleted += 1
        if note.is_private:
            activity.private_notes -= 1

        db.delete(note)
        db.commit()
        return {"message": f"Note '{note_id}' deleted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

# Custom exception handler
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Custom handler for HTTP exceptions, particularly 404 errors."""
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"detail": "Custom 404 - Resource not found"}
        )
    return await request.app.default_exception_handler(request, exc)