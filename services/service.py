from datetime import datetime
from models.api_model import DataTransferRateResponse, DataTransferRateRequest
from typing import List, Optional 
from services.mqtt_service import MQTTService
from utils.wireless_channels import get_channel_regions, get_region
from utils.things import get_thing_id_by_ip
from models.mqtt_model import ClientCommand, ForwarderCommand, ServerCommand


def get_data_transfer_rate(source: str, destination: str, path: List[str], wireless_channel: Optional[int], mqtt_service: MQTTService) -> DataTransferRateResponse:

    # we take the region for a specific wireless channel
    regions = get_channel_regions(wireless_channel)

    #normally we will deal with a tuple or a single tuple object
    region = get_region(regions)

    # we send the server command first

    destination_id = get_thing_id_by_ip(destination)

    region = "GR"

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

    # 4. Wait for telemetry result from the source device
    # This assumes mqtt_service has access to recent telemetry data, e.g., via an internal dictionary
    rate_mbps = None
    timeout = 5000  # seconds
    polling_interval = 0.5
    waited = 0

    while waited < timeout:
        telemetry = mqtt_service.get_telemetry(source_id)
        if telemetry and telemetry.get("wireless_channel") == wireless_channel:
            rate_mbps = telemetry.get("sent_rate_mbps")
            break
        time.sleep(polling_interval)
        waited += polling_interval

    if rate_mbps is None:
        raise RuntimeError(f"No telemetry received from device {source_id} within {timeout} seconds.")

   
    

    return DataTransferRateResponse(
        source=source,
        destination=destination,
        rate_mbps=rate_mbps,
        wireless_channel = wireless_channel,
        timestamp=datetime.utcnow().isoformat()
    )
