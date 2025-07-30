from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from libs.db.db import SessionLocal

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
    if tag:
        query = db.execute(
            "SELECT * FROM startups WHERE tags @> :tag LIMIT :limit",
            {"tag": [tag], "limit": limit},
        )
    else:
        query = db.execute(
            "SELECT * FROM startups LIMIT :limit",
            {"limit": limit},
        )
    return [dict(r) for r in query]