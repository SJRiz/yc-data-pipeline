from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from libs.app_config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()