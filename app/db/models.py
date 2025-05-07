from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, unique=True)
    invoice_number = Column(String)
    invoice_date = Column(String)
    total_amount = Column(String)
    vendor_name = Column(String)
    billing_address = Column(Text)
    shipping_address = Column(Text)
    created_at = Column(TIMESTAMP)
