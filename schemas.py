from pydantic import BaseModel


class AgentCreate(BaseModel):
    name: str
    budget: float


class AgentResponse(BaseModel):
    id: int
    name: str
    budget: float
    spent: float
    status: str
    api_key: str

    

    class Config:
        from_attributes = True

class SpendRequest(BaseModel):
    agent_id: int
    service: str
    amount: float
    api_key: str

class SpendRequestAPI(BaseModel):
    api_key: str
    service: str
    amount: float


class TransactionResponse(BaseModel):

    id: int
    agent_id: int
    service: str
    amount: float
    status: str

    class Config:
        from_attributes = True

class PolicyCreate(BaseModel):
    service: str
    max_amount: float
    action: str


class PolicyResponse(BaseModel):
    id: int
    service: str
    max_amount: float
    action: str

    class Config:
        from_attributes = True