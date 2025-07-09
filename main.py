from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TenantData(BaseModel):
    income: float
    rent: float
    on_time_payments: float  # percentage 0-100
    lease_months: int
    eviction_history: bool

@app.post("/score")
def calculate_score(data: TenantData):
    score = 0

    # Example weights
    income_ratio = data.income / data.rent
    if income_ratio >= 3:
        score += 40
    elif income_ratio >= 2.5:
        score += 30
    else:
        score += 15

    score += (data.on_time_payments / 100) * 30

    if data.lease_months >= 12:
        score += 20
    elif data.lease_months >= 6:
        score += 10

    if data.eviction_history:
        score -= 30

    # Clamp score between 0 and 100
    score = max(0, min(score, 100))

    return {"tenant_score": score}

# Goes to Tenant Score API Root
@app.get("/")
def read_root():
    return {
        "message": "Tenant Score API is alive!",
        "docs_url": "/docs"
    }