from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from policy_engine import check_spending
from blockchain import create_blockchain_record
from payment import verify_payment
from risk_engine import calculate_risk

from database import engine, Base, SessionLocal
from auth.routes import router as auth_router

import models
import schemas


# ==========================
# CREATE DATABASE TABLES
# ==========================

Base.metadata.create_all(bind=engine)


# ==========================
# FASTAPI APPLICATION
# ==========================

app = FastAPI(
    title="SentinelX API",
    description="AI Agent Spending Firewall",
    version="1.0"
)

app.include_router(auth_router)


# ==========================
# CORS CONFIGURATION
# ==========================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================
# DATABASE CONNECTION
# ==========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================
# HOME API
# ==========================

@app.get("/")
def home():

    return {
        "project": "SentinelX",
        "message": "AI Agent Spending Firewall Running"
    }


# ==========================
# CREATE AI AGENT
# ==========================

@app.post("/agents", response_model=schemas.AgentResponse)
def create_agent(
    agent: schemas.AgentCreate,
    db: Session = Depends(get_db)
):

    new_agent = models.Agent(
        name=agent.name,
        budget=agent.budget
    )

    db.add(new_agent)

    db.commit()

    db.refresh(new_agent)

    return new_agent


# ==========================
# SPENDING REQUEST API
# ==========================

@app.post("/spend")
def request_spending(
    request: schemas.SpendRequest,
    db: Session = Depends(get_db)
):

    # Find AI Agent

    agent = db.query(models.Agent).filter(
        models.Agent.id == request.agent_id
    ).first()

    if not agent:

        return {
            "error": "Agent not found"
        }


    # ==========================
    # API KEY VERIFICATION
    # ==========================

    if agent.api_key != request.api_key:

        return {
            "error": "Invalid API key",
            "status": "UNAUTHORIZED"
        }


    # ==========================
    # CHECK SPENDING POLICY
    # ==========================

    decision = check_spending(
        agent,
        request.service,
        request.amount
    )

    blockchain_hash = None


    # ==========================
    # APPROVE / BLOCK
    # ==========================

    if decision["approved"]:

        status = "APPROVED"

        # Update spending

        agent.spent += request.amount

        # Blockchain proof

        blockchain_hash = create_blockchain_record({

            "agent_id": request.agent_id,

            "service": request.service,

            "amount": request.amount,

            "status": status

        })

    else:

        status = "BLOCKED"


    # ==========================
    # CALCULATE RISK
    # ==========================

    risk_score = calculate_risk(
        request.amount
    )


    # ==========================
    # STORE TRANSACTION
    # ==========================

    transaction = models.Transaction(

        agent_id=request.agent_id,

        service=request.service,

        amount=request.amount,

        status=status,

        blockchain_hash=blockchain_hash,

        risk_score=risk_score
    )

    db.add(transaction)

    db.commit()

    db.refresh(transaction)


    # ==========================
    # RESPONSE
    # ==========================

    return {

        "transaction_id": transaction.id,

        "agent_id": transaction.agent_id,

        "service": transaction.service,

        "amount": transaction.amount,

        "status": transaction.status,

        "blockchain_hash": transaction.blockchain_hash,

        "risk_score": transaction.risk_score,

        "reason": decision["reason"]

    }


# ==========================
# API KEY SPENDING REQUEST
# ==========================

@app.post("/spend-api")
def spend_using_api_key(
    request: schemas.SpendRequestAPI,
    db: Session = Depends(get_db)
):

    # Find AI Agent using API Key

    agent = db.query(models.Agent).filter(
        models.Agent.api_key == request.api_key
    ).first()


    if not agent:

        return {
            "error": "Invalid API Key",
            "status": "UNAUTHORIZED"
        }


    # ==========================
    # CHECK POLICY
    # ==========================

    decision = check_spending(
        agent,
        request.service,
        request.amount
    )

    blockchain_hash = None


    # ==========================
    # APPROVE / BLOCK
    # ==========================

    if decision["approved"]:

        status = "APPROVED"

        agent.spent += request.amount

        blockchain_hash = create_blockchain_record({

            "agent_id": agent.id,

            "service": request.service,

            "amount": request.amount,

            "status": status

        })

    else:

        status = "BLOCKED"


    # ==========================
    # RISK SCORE
    # ==========================

    risk_score = calculate_risk(
        request.amount
    )


    # ==========================
    # STORE TRANSACTION
    # ==========================

    transaction = models.Transaction(

        agent_id=agent.id,

        service=request.service,

        amount=request.amount,

        status=status,

        blockchain_hash=blockchain_hash,

        risk_score=risk_score
    )

    db.add(transaction)

    db.commit()

    db.refresh(transaction)


    return {

        "agent": agent.name,

        "status": status,

        "amount": request.amount,

        "risk_score": risk_score,

        "reason": decision["reason"],

        "blockchain_hash": blockchain_hash

    }


# ==========================
# x402 PAYMENT API
# ==========================

@app.get("/paid-service")
def paid_service(payment_status: str):

    verify_payment(payment_status)

    return {

        "message": "Service access granted",

        "payment": "verified"

    }


# ==========================
# DASHBOARD API
# ==========================

@app.get("/dashboard")
def dashboard_data(
    db: Session = Depends(get_db)
):

    total_agents = db.query(
        models.Agent
    ).count()


    approved = db.query(
        models.Transaction
    ).filter(
        models.Transaction.status == "APPROVED"
    ).count()


    blocked = db.query(
        models.Transaction
    ).filter(
        models.Transaction.status == "BLOCKED"
    ).count()


    transactions = db.query(
        models.Transaction
    ).all()


    return {

        "total_agents": total_agents,

        "approved_transactions": approved,

        "blocked_transactions": blocked,

        "transactions": [

            {
                "service": t.service,

                "amount": t.amount,

                "status": t.status,

                "risk_score": t.risk_score,

                "hash": t.blockchain_hash,

                "created_at": t.created_at
            }

            for t in transactions

        ]

    }


# ==========================
# GET ALL AGENTS
# ==========================

@app.get("/agents")
def get_agents(
    db: Session = Depends(get_db)
):

    agents = db.query(
        models.Agent
    ).all()

    return agents


# ==========================
# CREATE POLICY
# ==========================

@app.post(
    "/policies",
    response_model=schemas.PolicyResponse
)
def create_policy(
    policy: schemas.PolicyCreate,
    db: Session = Depends(get_db)
):

    new_policy = models.Policy(

        service=policy.service,

        max_amount=policy.max_amount,

        action=policy.action

    )

    db.add(new_policy)

    db.commit()

    db.refresh(new_policy)

    return new_policy


# ==========================
# GET ALL POLICIES
# ==========================

@app.get("/policies")
def get_policies(
    db: Session = Depends(get_db)
):

    return db.query(
        models.Policy
    ).all()