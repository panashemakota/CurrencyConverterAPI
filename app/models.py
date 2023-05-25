from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime, date
from hashlib import md5

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
    first_name = Column(String(30))
    last_name = Column(String(30))
    username = Column(String(25))
    email = Column(String(50))
    raw_password = Column(String(256))
    country_id = Column(Integer, ForeignKey("countries.id"))
    date_created = Column(DateTime,  default=datetime.utcnow)
    
    @property
    def password(self):
        hash_object = md5(self.raw_password.encode())
        result = hash_object.hexdigest()
        return result
    
    @password.setter
    def password(self, value):
        size = len(value)
        if size >= 8 and size <= 20:
            hash_object = md5(value.encode())
            self.raw_password = hash_object.hexdigest()
        else:
            print("Password should be between 8 to 20 characters")
            raise ValueError

    def local_date():
        return