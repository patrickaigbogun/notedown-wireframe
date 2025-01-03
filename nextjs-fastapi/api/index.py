from fastapi import FastAPI, HTTPException, status, Depends, Form
from pydantic import BaseModel, EmailStr, Field
from database.models import User, UserActivity, Note
from database.main import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
import uuid
from datetime import datetime

app = FastAPI()

# Allow all origins for demo purposes (you should adjust this for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input Models
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

class NoteResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    is_private: bool
    created_at: datetime

def hash_password_with_id(password: str, user_id: str) -> str:
    """Hash a plain-text password using the user's unique ID as part of the salt."""
    combined = f"{password}{user_id}"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(combined.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password_with_id(plain_password: str, user_id: str, hashed_password: str) -> bool:
    """Verify a password against a hash using the user's unique ID as part of the salt."""
    combined = f"{plain_password}{user_id}"
    return bcrypt.checkpw(combined.encode('utf-8'), hashed_password.encode('utf-8'))

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, db: Session = Depends(get_db)):
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
                raise HTTPException(status_code=400, detail="The username you provided is already in use. Please choose a different username.")
            if "email" in str(e.orig):
                raise HTTPException(status_code=400, detail="The email address you provided is already registered. Please use a different email address.")
        raise HTTPException(status_code=400, detail="A database integrity error occurred during registration. Please try again.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"An unexpected error occurred during registration: {str(e)}")

@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    if not user.username or not user.password:
        raise HTTPException(status_code=400, detail="Both username and password are required to log in.")
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and verify_password_with_id(user.password, str(db_user.id), db_user.password):
        return {"message": f"Login successful! Welcome back, {user.username}."}
    raise HTTPException(status_code=400, detail="Invalid username or password. Please check your credentials and try again.")

@app.post("/create_note/{user_id}", response_model=NoteResponse)
async def create_note(user_id: uuid.UUID, note: NoteCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"No user found with the ID '{user_id}'. Please provide a valid user ID.")
    
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
        raise HTTPException(status_code=400, detail=f"Failed to create note: {str(e)}")

@app.delete("/delete_note/{note_id}")
async def delete_note(note_id: uuid.UUID, user_id: uuid.UUID, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"No user found with the ID '{user_id}'. Please provide a valid user ID.")
    
    note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"No note found with the ID '{note_id}' associated with the user ID '{user_id}'.")
    
    try:
        activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).first()
        activity.notes_deleted += 1
        if note.is_private:
            activity.private_notes -= 1

        db.delete(note)
        db.commit()
        return {"message": f"Note with ID '{note_id}' has been successfully deleted."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete note: {str(e)}")