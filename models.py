from pydantic import BaseModel
from typing import Optional


class DataTransferRateResponse(BaseModel):
    source: str
    destination: str
    rate_mbps: float
    timestamp: Optional[str] = None
