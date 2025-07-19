# schemas.py

from pydantic import BaseModel
from typing import Optional

class ClientCommand(BaseModel):
    device_id: str
    wireless_channel: int
    region: str
    ip_server: str
    ip_routing: Optional[str]

class ForwarderCommand(BaseModel):
    device_id: str
    wireless_channel: int
    region: str
    ip_routing: str

class ServerCommand(BaseModel):
    device_id: str
    wireless_channel: int
    region: str
