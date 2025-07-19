from datetime import datetime
from models.api_model import DataTransferRateResponse, DataTransferRateRequest
from typing import List, Optional 
from services.mqtt_service import MQTTService


def get_data_transfer_rate(source: str, destination: str, path: List[str], wireless_channel: Optional[int], mqtt_service: MQTTService) -> DataTransferRateResponse:

    # we take the region for a specific wireless channel
    regions = get_channel_regions(wireless_channel)

    #normally we will deal with a tuple or a single tuple object
    region = get_region(regions)

    # we send the server command first

    destination_id = get_thing_id_by_ip(destination)

    server_cmd = ServerCommand (
        device_id=destination_id,
        wireless_channel=wireless_channel,
        region=region
    )
    mqtt_service.send_command(server_cmd)

    # we send the forwarder commands
    next_hops = list(path[1:]) + [destination]
    for intermediate_ip, next_ip in zip(filter(None, path), next_hops):
        intermediate_id = get_thing_id_by_ip(intermediate_ip)
        forwarder_cmd = ForwarderCommand(
            device_id=intermediate_id,
            wireless_channel=wireless_channel,
            region=region,
            ip_routing=next_ip
        )
        mqtt_service.send_command(forwarder_cmd)


    #we send the client command
    source_id = get_thing_id_by_ip(source)
    client_cmd = ClientCommand(
        device_id=source_id,
        wireless_channel=wireless_channel,
        region=region,
        ip_server=destination,
        ip_routing=path[0] if path else None
    )
    mqtt_service.send_command(client_cmd)

    #here we are subscribed to the response topic to receive the response from the source node
    """ 
    async for state in get_digital_twin_state():
        if thing_id = state,get(source_id):
            #something similar
            neighbors = state.get("features", {}).get("network", {}).get("properties", {}).get("neighbors", [])
            break"""
    

    return DataTransferRateResponse(
        source=source,
        destination=destination,
        rate_mbps=rate_mbps,
        wireless_channel = wireless_channel,
        timestamp=datetime.utcnow().isoformat()
    )
