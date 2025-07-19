from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from models.api_model import DataTransferRateResponse, DataTransferRateRequest, HealthCheckResponse
from services.service import get_data_transfer_rate
import time
import random
from datetime import datetime


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


# --- NEW: Health Check Endpoint ---
@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """
    Performs a simple health check on the API.
    Returns current status, message, and timestamp.
    """
    # Using current Unix timestamp in milliseconds for consistency
    return HealthCheckResponse(
        status="ok",
        message="Network API is up and running.",
        timestamp=int(time.time() * 1000)
    )

@router.post("/data-transfer-rate-2", response_model=DataTransferRateResponse)
def simulate_data_transfer_rate_response(request: DataTransferRateRequest):
    """
    Receives data transfer rate parameters and simulates a DataTransferRateResponse.
    This endpoint is for testing/simulation and does NOT call actual services.
    """
    print("\n--- /data-transfer-rate-2 (SIMULATED RESPONSE MODE) ---")
    print(f"  Received Source: {request.source}")
    print(f"  Received Destination: {request.destination}")
    print(f"  Received Path: {request.path}")
    print(f"  Received Wireless Channel: {request.wireless_channel}")
    print("--- END SIMULATION ---\n")

    # Generate a random rate_mbps
    simulated_rate_mbps = round(random.uniform(50.0, 900.0), 2)

    # Return a DataTransferRateResponse object
    return DataTransferRateResponse(
        source=request.source,
        destination=request.destination,
        path=request.path, # Ensure path is included, as it's part of the model
        wireless_channel=request.wireless_channel,
        rate_mbps=simulated_rate_mbps,
        timestamp=int(datetime.utcnow().timestamp() * 1000) # Use Unix timestamp in ms for consistency
    )   