from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional from models import DataTransferRateResponse
from servcies import get_data_transfer_rate


router = APIRouter(prefix="/network", tags=["network"])


@router.post("/data-transfer-rate", response_model=DataTransferRateResponse)
def get_data_transfer_rate_endpoint(request: DataTransferRateRequest):
    """
    Get data transfer rate measurements between source and destination through specified path.
    All nodes in the path use the same wireless channel if specified.
    """

    try:
        data = get_data_transfer_rate(
            source=request.source,
            destination=request.destination,
            path=request.path,
            wireless_channel=request.wireless_channel
        )
        # Save to file, if needed
        save_data_transfer_rate_to_file(data, "./data_transfer_log.csv")
        return data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
