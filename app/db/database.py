from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update this based on your system
DATABASE_URL = "postgresql://:apoorvareddybachugudam@localhost/invoice_parser_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
