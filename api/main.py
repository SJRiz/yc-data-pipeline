from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from db.sql import SessionLocal

# Create the fast api app
app = FastAPI()

# Get the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Api route to get all startups
@app.get("/startups/")
def read_startups(tag: str = None, limit: int = 20, db: Session = Depends(get_db)):
    query = db.execute("SELECT * FROM startups WHERE ($1 IS NULL OR tags @> ARRAY[$1]) LIMIT $2", (tag, limit))
    return [dict(r) for r in query]