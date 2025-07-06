from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import json
import logging
from ditto.Ditto.service import get_digital_twin_state, send_message_to_ditto
from ditto.Ditto.exceptions import DittoAPIException, NetworkPropertiesValidationError, EventStreamParseException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ditto", tags=["ditto"])


class MessagePayload(BaseModel):
    """Request model for sending messages to digital twin"""
    data: Dict[str, Any]


@router.get("/digital-twins/state")
async def stream_digital_twin_state():
    """
    Stream digital twin state changes via Server-Sent Events.
    
    Returns:
        StreamingResponse: Event stream of digital twin state changes
    """
    try:
        async def event_stream():
            async for state_data in get_digital_twin_state():
                if state_data:  # Only yield non-empty data
                    yield f"data: {json.dumps(state_data)}\n\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
            }
        )
    except DittoAPIException as e:
        logger.error(f"Ditto API error: {e}")
        raise HTTPException(status_code=500, detail=f"Ditto API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error streaming digital twin state: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/digital-twins/{twin_id}/messages/olsr-reconfigure")
async def send_olsr_reconfigure_message(
    twin_id: str,
    payload: MessagePayload
):
    """
    Send OLSR reconfiguration message to a specific digital twin.
    
    Args:
        twin_id: The ID of the digital twin
        payload: The message payload containing reconfiguration data
        
    Returns:
        dict: Response from the digital twin
    """
    try:
        response = await send_message_to_ditto(payload.data, twin_id)
        return {
            "status": "success",
            "twin_id": twin_id,
            "response": response
        }
    except DittoAPIException as e:
        logger.error(f"Ditto API error for twin {twin_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Ditto API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error sending message to twin {twin_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/digital-twins/{twin_id}/status")
async def get_digital_twin_status(twin_id: str):
    """
    Get the current status of a specific digital twin.
    
    Args:
        twin_id: The ID of the digital twin
        
    Returns:
        dict: Status information for the digital twin
    """
    # This is a placeholder endpoint - you may want to implement
    # a specific service function to get individual twin status
    return {
        "twin_id": twin_id,
        "status": "active",
        "message": "Use the /digital-twins/state endpoint to stream real-time state changes"
    }


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the Ditto service.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "service": "ditto-digital-twin-service"
    }