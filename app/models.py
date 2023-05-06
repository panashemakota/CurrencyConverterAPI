from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from . import Base
import datetime

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    iso = Column(String(3))
    valuation = Column(Float)
    country = Column(String(50))
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)

    def local_date():
        return
    
class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    valuation = Column(Float)
    country = Column(String(50), unique=True)
    date = Column(Date,  default=datetime.date.today)

    def local_date():
        return
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    valuation = Column(Float)
    country = Column(String(50))
    date_created = Column(DateTime,  default=datetime.datetime.utcnow)

    def local_date():
        return