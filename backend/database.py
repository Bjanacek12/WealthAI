from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Numeric, Text, Enum
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///./wealthai.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tables

class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key = True, index = True)
    email = Column(String, unique = True, index = True, nullable = False)
    password_hash = Column(String, nullable = False)
    role = Column(String, default = "Junior Adviosor")
    created_at = Column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))

    clients = relationship("Client", back_populates = "manager")

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
    manager_id = Column(Integer, ForeignKey("managers.id"))
    first_name = Column(String)
    last_name = Column(String)
    risk_score = Column(Integer)
    investment_goal = Column(String)
    is_active = Column(Boolean, default = True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    household = relationship("Household", back_populates="clients")
    manager = relationship("Manager", back_populates = "clients")
    goals = relationship("Goal", back_populates="client")
    portfolios = relationship("Portfolio", back_populates = "client")
    interactions = relationship("Interaction", back_populates = "client")

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key = True, index = True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    target_amount = Column(Numeric(12, 2))
    target_date = Column(DateTime)
    description = Column(String)
    priority = Column(Integer, default = 5)    #1-10 scale
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    client = relationship("Client", back_populates="goals")

class Portfolio(Base):
    __tablename__= "portfolios"
    id = Column(Integer, primary_key = True, index = True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    account_number = Column(String, unique = True)     #Need to mask
    total_value = Column(Numeric(15, 2))
    created_at = Column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))

    client = relationship("Client", back_populates = "portfolios")
    positions = relationship("Position", back_populates =  "portfolio")

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key = True, index = True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    ticker = Column(String(10), index = True, nullable = False)
    quantity = Column(Numeric(18, 4))
    cost_basis = Column(Numeric(18, 2))
    position_type = Column(String)   # Can be equity, fixed_income, cash
    created_at = Column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))

    portfolio = relationship("Portfolio", back_populates = "positions")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key = True, index = True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    type = Column(String)   # email, call, voice note
    raw_content = Column(Text)
    vector_id = Column(String, index = True)  # Link to Azure AI search
    created_at = Column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))

    client = relationship("Client", back_populates = "interactions")
    sentiment_log = relationship("SentimentLog", back_populates = "interactions")

class SentimentLog(Base):
    __tablename__ = "sentiment_logs"
    id = Column(Integer, primary_key = True, index = True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"))
    sentiment_score = Column(Float)   # -1.0 to 1.0
    summary = Column(Text)
    created_at = Column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))

    interaction = relationship("Interaction", back_populates= "sentiment_log")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key = True, index = True)
    manager_id = Column(Integer, ForeignKey("managers.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    action = Column(String)   # View, generate_pdf
    timestamp = Column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))

class ActionItem(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key = True, index = True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    status = Column(String, default = "Pending")   #pending, completed
    ai_rationale = Column(Text)
    created_at = Column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))


def init_db():
    Base.metadata.create_all(bind=engine)