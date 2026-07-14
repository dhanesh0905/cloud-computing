from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
import uuid

API_KEY_NAME = "X-API-Key"
DUMMY_API_KEY = "super-secret-exam-key-2026"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="Cloud Payment Microservice",
    description="A simple microservice to process payments for a cloud computing exam.",
    version="1.0.0"
)
class PaymentRequest(BaseModel):
    user_id: str = Field(..., description="The ID of the user making the payment")
    amount: float = Field(..., gt=0, description="Payment amount (must be greater than 0)")
    currency: str = Field(..., min_length=3, max_length=3, description="3-letter currency code (e.g., USD, EUR)")

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str
    message: str

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """Validates the API key provided in the request headers."""
    if api_key_header != DUMMY_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )
    return api_key_header

@app.post("/api/v1/payments", response_model=PaymentResponse)
async def process_payment(
    request: PaymentRequest, 
    api_key: str = Depends(get_api_key)
):
    """
    Processes a payment.
    Requires a valid JSON payload and an X-API-Key header.
    """

    transaction_id = str(uuid.uuid4())
    
    return PaymentResponse(
        transaction_id=transaction_id,
        status="SUCCESS",
        message=f"Successfully processed {request.amount} {request.currency} for user {request.user_id}"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint for cloud load balancers / Kubernetes."""
    return {"status": "healthy"}