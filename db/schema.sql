CREATE TABLE IF NOT EXISTS startups (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    slug TEXT UNIQUE,
    ceo_name TEXT,
    ceo_linkedin TEXT,
    company_linkedin TEXT,
    eng BOOLEAN,
    remote BOOLEAN,
    job_website TEXT,
    desc TEXT,
    stage TEXT,
    tags TEXT[],
    industries TEXT[],
    all_locations TEXT,
    team_size INT,
    batch TEXT,
    funding BIGINT
    last_scraped_at TIMESTAMP DEFAULT NOW()
)