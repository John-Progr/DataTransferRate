from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional from models import DataTransferRateResponse
from servcies import get_data_transfer_rate


router = APIRouter(prefix="/network", tags=["network"])

@router.get("/data-transfer-rate", response_model=DataTransferRateResponse)
def get_data_transfer_rate_endpoint(
    source: str,
    destination: str,
    path: List[str],
    wireless_channel: Optional[int] = None
):
    """
     Get data transfer rate measurements between source and destination through specified path.

     All nodes in the path use the same wireless channel if specified.

     """

     try:
        data = get_data_transfer_rate(
            source=source,
            destination=destination,
            path=path,
            wireless_channel=wireless_channel
        )
        log_data = save_data_transfer_rate_to_file(DataTransferRateResponse,"./data_transfer_log.csv")
    except ValueError as e:
        raise_bad_request(str(e))
    except Exception as e:
        raise_internan_server_error()



