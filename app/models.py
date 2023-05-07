from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime, date

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    iso = Column(String(3), unique=True)
    valuation = Column(Float)
    country_id = Column(Integer, ForeignKey("countries.id"))
    date_created = Column(DateTime,  default=datetime.utcnow)

    country = relationship("Country", backref="Currency.country_id")

    def local_date():
        return
    
class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    date_created = Column(DateTime,  default=datetime.utcnow)

    def local_date():
        return
    
class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey("currencies.id"))
    valuation = Column(Float)
    country_id = Column(Integer, ForeignKey("countries.id"))
    date = Column(Date,  default=date.today)

    country = relationship("Country", backref="Performance.country_id")
    currency = relationship("Currency", backref="Performance.currency_id")

    def local_date():
        return
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    valuation = Column(Float)
    country_id = Column(Integer, ForeignKey("countries.id"))
    date_created = Column(DateTime,  default=datetime.utcnow)

    def local_date():
        return