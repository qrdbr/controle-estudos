from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.api.control_routes import router as control_router

app: FastAPI = FastAPI(
    title="Controle de Estudos API",
    description="MVP de micro-API para gestão de controle de estudos (trilha, curso da trilha e atividades de estudo do curso)",
    version="0.1.0"
)

app.include_router(control_router, prefix="/api/v1")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Status da API")
    timestamp: str = Field(..., description="Timestamp UTC ISO8601")

@app.get("/health", response_model=HealthResponse, summary="Healthcheck", tags=["Health"])
def healthcheck() -> HealthResponse:
    """Endpoint para verificação de status da API."""
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow().isoformat()
    )
