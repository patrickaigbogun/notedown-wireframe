from fastapi import FastAPI, HTTPException, status, Depends, Form
from pydantic import BaseModel
from database.models import User, UserActivity, Note
from database.main import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import bcrypt


import uuid
app = FastAPI()

# Allow all origins for demo purposes (you should adjust this for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set specific allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # or set specific allowed methods
    allow_headers=["*"],  # or set specific allowed headers
)


class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class NoteCreate(BaseModel):
    title: str
    content: str
    is_private: bool = False

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    is_private: bool
    created_at: str




def hash_password_with_id(password: str, user_id: str) -> str:
    """Hash a plain-text password using the user's unique ID as part of the salt."""
    # Combine the password and user_id
    combined = f"{password}{user_id}"
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(combined.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password_with_id(plain_password: str, user_id: str, hashed_password: str) -> bool:
    """Verify a password against a hash using the user's unique ID as part of the salt."""
    combined = f"{plain_password}{user_id}"
    return bcrypt.checkpw(combined.encode('utf-8'), hashed_password.encode('utf-8'))


@app.post("/register", status_code=status.HTTP_200_OK)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        # Generate a unique user ID
        user_id = str(uuid.uuid4())
        
        # Hash the password with the user ID
        hashed_password = hash_password_with_id(user.password, user_id)
        
        new_user = User(
            id=user_id,
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        db.add(new_user)
        
        # Create associated activity record
        activity = UserActivity(user_id=user_id)
        db.add(activity)
        
        db.commit()
        return {"message": "User registered successfully", "user_id": user_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user and verify_password_with_id(user.password, str(db_user.id), db_user.password):
            return {"message": "Login successful"}
        raise HTTPException(status_code=400, detail="Invalid credentials")
    except:
        raise HTTPException(status_code=400, detail="Login failed")



@app.get("/get_user_activity/{user_id}")
async def get_activity(user_id: uuid.UUID, db: Session = Depends(get_db)):
    activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@app.post("/create_note/{user_id}")
async def create_note(user_id: uuid.UUID, note: NoteCreate, db: Session = Depends(get_db)):
    try:
        new_note = Note(
            id=uuid.uuid4(),
            user_id=user_id,
            title=note.title,
            content=note.content,
            is_private=note.is_private
        )
        db.add(new_note)
        
        # Update user activity
        activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).first()
        activity.notes_created += 1
        if note.is_private:
            activity.private_notes += 1
            
        db.commit()
        return {"message": "Note created successfully", "note_id": str(new_note.id)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to create note: {str(e)}")

@app.get("/get_notes/{user_id}", response_model=List[NoteResponse])
async def get_notes(user_id: uuid.UUID, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    if not notes:
        return []
    return notes

@app.get("/get_user_activity/{user_id}")
async def get_activity(user_id: uuid.UUID, db: Session = Depends(get_db)):
    activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@app.delete("/delete_note/{note_id}")
async def delete_note(note_id: uuid.UUID, user_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        note = db.query(Note).filter(Note.id == note_id, Note.user_id == user_id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
            
        # Update activity
        activity = db.query(UserActivity).filter(UserActivity.user_id == user_id).first()
        activity.notes_deleted += 1
        if note.is_private:
            activity.private_notes -= 1
            
        db.delete(note)
        db.commit()
        return {"message": "Note deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to delete note: {str(e)}")