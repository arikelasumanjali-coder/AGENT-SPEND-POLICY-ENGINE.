from database import SessionLocal
import models


def check_spending(agent, service, amount):

    db = SessionLocal()

    policy = db.query(models.Policy).filter(
        models.Policy.service == service
    ).first()

    db.close()

    if not policy:
        return {
            "approved": False,
            "reason": "No policy found for this service"
        }

    if policy.action == "BLOCK":
        return {
            "approved": False,
            "reason": "Service blocked by policy"
        }

    if amount > policy.max_amount:
        return {
            "approved": False,
            "reason": "Policy spending limit exceeded"
        }

    remaining = agent.budget - agent.spent

    if amount > remaining:
        return {
            "approved": False,
            "reason": "Agent budget exceeded"
        }

    return {
        "approved": True,
        "reason": "Policy Approved"
    }