import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

# Create SQLAlchemy engine
engine = create_engine(os.getenv('DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def setup_database():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cur = conn.cursor()
    
    # Read and execute SQL file
    with open('schema.sql', 'r') as file:
        cur.execute(file.read())
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_database()
