from datetime import datetime
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    service: str
    now: datetime