from typing import Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
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

# Api route to get startups with specified params
@app.get("/startups/")
def read_startups(
    tag: Optional[str] = None,
    min_funding: int = Query(0, ge=0),
    max_funding: int = Query(int(1e12), ge=0),
    limit: int = Query(100, ge=0),
    db: Session = Depends(get_db),
):
    sql = """
    SELECT 
        name AS "Company",
        ceo_name AS "CEO",
        funding,
        stage,
        team_size,
        tags,
        industries,
        eng AS "Hiring eng",
        remote AS "Hiring remote",
        all_locations AS locations,
        job_website,
        company_linkedin,
        ceo_linkedin,
        description,
        batch
    FROM startups
    WHERE funding BETWEEN :min_funding AND :max_funding
    """

    params = {"min_funding": min_funding, "max_funding": max_funding}

    if tag:
        sql += " AND tags @> :tag"
        params["tag"] = [tag]  # array syntax expected for PostgreSQL

    if limit > 0:
        sql += " LIMIT :limit"
        params["limit"] = limit

    query = db.execute(text(sql), params)
    return [dict(r) for r in query]