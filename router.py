from fastapi import APIRouter, Query
from typing import Optional

from models import DataTransferRateResponse
from services import get_data_transfer_rate

router = APIRouter()


@router.get("/dataTransferRate", response_model=DataTransferRateResponse)
def read_data_transfer_rate(
    source: str = Query(..., description="Source of the data transfer"),
    destination: str = Query(..., description="Destination of the data transfer")
):
    """
    Retrieve data transfer rate between source and destination.
    """
    return get_data_transfer_rate(source, destination)
