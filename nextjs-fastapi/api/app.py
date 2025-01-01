from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from database.models import User, UserActivity, Note
from database.main import get_db
from sqlalchemy.orm import Session
from typing import List


import uuid

app = FastAPI()



class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
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



@app.post("/register", status_code=status.HTTP_200_OK)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        user_id = uuid.uuid4()
        new_user = User(
            id=user_id,
            username=user.username,
            email=user.email,
            password=user.password
        )
        db.add(new_user)
        
        # Create associated activity record with the proper UUID
        activity = UserActivity(user_id=user_id)
        db.add(activity)
        
        db.commit()
        return {"message": "User registered successfully", "user_id": str(user_id)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user and db_user.password == user.password:
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