from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    activity = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")

class UserActivity(Base):
    __tablename__ = 'user_activity'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    notes_created = Column(Integer, default=0)
    notes_deleted = Column(Integer, default=0)
    notes_shared = Column(Integer, default=0)
    times_logged_in = Column(Integer, default=0)
    private_notes = Column(Integer, default=0)
    
    user = relationship("User", back_populates="activity")


class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    user = relationship("User", backref="notes")

