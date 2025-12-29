from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///./wealthai.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tables

class Household(Base):
    __tablename__ = "households"
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    clients = relationship("Client", back_populates = "household")

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    first_name = Column(String)
    last_name = Column(String)
    risk_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    household = relationship("Household", back_populates="clients")
    goals = relationship("Goal", back_populates="client")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key = True, index = True)
    clent_id = Column(Integer, ForeignKey("clients.id"))
    target_amount = Column(Float)
    target_date = Column(DateTime)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    client = relationship("Client", back_populates="goals")

def init_db():
    Base.metadata.create_all(bind=engine)