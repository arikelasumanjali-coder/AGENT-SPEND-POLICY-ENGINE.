from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

password = quote_plus("Sumanjali@123")

DATABASE_URL = f"mysql+mysqlconnector://root:{password}@localhost:3306/sentinelx"

engine = create_engine(
    DATABASE_URL
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()