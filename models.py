from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
import secrets

from database import Base


# ===========================
# USERS
# ===========================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))

    email = Column(String(120), unique=True)

    password = Column(String(255))

    role = Column(String(50), default="admin")

    created_at = Column(DateTime, default=datetime.utcnow)


# ===========================
# AI AGENTS
# ===========================

class Agent(Base):

    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))

    budget = Column(Float)

    spent = Column(Float, default=0)

    status = Column(String(20), default="active")

    api_key = Column(
        String(255),
        unique=True,
        default=lambda: "sx_live_" + secrets.token_hex(16)
    )


# ===========================
# TRANSACTIONS
# ===========================

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    agent_id = Column(Integer)

    service = Column(String(100))

    amount = Column(Float)

    status = Column(String(20))

    blockchain_hash = Column(String(255), nullable=True)

    risk_score = Column(Float, default=0)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class Policy(Base):

    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)

    service = Column(String(100))

    max_amount = Column(Float)

    action = Column(String(20))