# from datetime import datetime
from datetime import datetime
import pytz
from sqlalchemy import (Column, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# datetime_ist = datetime.utcnow() + timedelta(hours=5, minutes=30)

datetime_ist = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

engine = create_engine('sqlite:///./core.db', echo=True, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Core(Base):
    __tablename__ = "core"
    id = Column(Integer, primary_key=True, index=True)
    customerName = Column(String, nullable=True)
    opportunityId = Column(String, nullable=True)
    projectName = Column(String, nullable=True)
    lob = Column(String, nullable=True)
    projectStartDate = Column(String, nullable=True)
    projectEndDate = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    planningType = Column(String, nullable=True)
    month = Column(String, nullable=True)
    week = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    level = Column(String, nullable=True)
    uniqueid = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)
    updated = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)


class CP(Base):
    __tablename__ = "cp"
    id = Column(Integer, primary_key=True, index=True)
    cpid = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)
    updated = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)


class GL(Base):
    __tablename__ = "GL"
    id = Column(Integer, primary_key=True, index=True)
    GLid = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)
    updated = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)


class RateCard(Base):
    __tablename__ = "rc"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=True)
    titles = Column(String, nullable=True)
    country = Column(String, nullable=True)
    year = Column(String, nullable=True)
    rate = Column(String, nullable=True)
    created = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)
    updated = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)


class CompanyRateCard(Base):
    __tablename__ = "crc"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=True)
    titles = Column(String, nullable=True)
    country = Column(String, nullable=True)
    year = Column(String, nullable=True)
    rate = Column(String, nullable=True)
    created = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)
    updated = Column(String, default=datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S'),
                     nullable=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
