# mqtt_router.py

from fastapi import APIRouter, Depends, HTTPException
from mqtt_dependencies import get_mqtt_client
from mqtt_models import CommandMessage
from mqtt_service import publish_status
import logging

router = APIRouter()

logger = logging.getLogger(__name__)




router = APIRouter()

@router.post("/be-client")
def be_client(cmd: ClientCommand, client = Depends(get_mqtt_client)):
    return send_client_command(client, cmd)

@router.post("/be-forwarder")
def be_forwarder(cmd: ForwarderCommand, client = Depends(get_mqtt_client)):
    return send_forwarder_command(client, cmd)

@router.post("/be-server")
def be_server(cmd: ServerCommand, client = Depends(get_mqtt_client)):
    return send_server_command(client, cmd)

@router.post("/commands/send")
async def send_command(cmd: CommandMessage, client=Depends(get_mqtt_client)):
    try:
        payload = cmd.json()
        client.publish("commands/device", payload)
        logger.info(f"Sent command: {payload}")
        return {"status": "success", "message": "Command sent"}
    except Exception as e:
        logger.error(f"Error sending command: {e}")
        raise HTTPException(status_code=500, detail="Failed to send command")

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mqtt-fastapi"}
