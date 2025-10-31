import logging
import time
from datetime import datetime
from models.api_model import DataTransferRateResponse, DataTransferRateRequest
from typing import List, Optional 
from services.mqtt_service import MQTTService
from utils.wireless_channels import get_channel_regions, get_region
from utils.things import get_thing_id_by_ip
from models.mqtt_model import ClientCommand, ForwarderCommand, ServerCommand

logger = logging.getLogger(__name__)


def get_data_transfer_rate(
    source: str,
    destination: str,
    path: List[str],
    wireless_channel: Optional[int],
    mqtt_service: MQTTService
) -> DataTransferRateResponse:
    """
    Measure data transfer rate 10 times, sending server, forwarder, and client commands each iteration,
    and return the average throughput.
    """

    repeats = 1 # fixed number of measurements
    region = get_channel_regions(wireless_channel) # hardcoded region

    # get IDs
    source_id = get_thing_id_by_ip(source)
    destination_id = get_thing_id_by_ip(destination)

    rates: List[float] = []

    for i in range(repeats):
        print(f"🔄 Measurement {i+1}/{repeats}")

        # --- Send server command ---
        server_cmd = ServerCommand(
            device_id=destination_id,
            wireless_channel=wireless_channel,
            region=region
        )
        mqtt_service.send_command(server_cmd)

        if path:
            # --- Send forwarder commands ---
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

        # --- Send client command ---
        client_cmd = ClientCommand(
            device_id=source_id,
            wireless_channel=wireless_channel,
            region=region,
            ip_server=destination,
            ip_routing=path[0] if path else destination
        )

        time.sleep(4)  # optional delay before sending client command
        mqtt_service.send_command(client_cmd)

        # wait for telemetry
        message = mqtt_service.wait_for_message("telemetry", timeout=30.0)
        rate_mbps = message["sent_rate_mbps"]

        print(f"✅ Iteration {i+1}: throughput = {rate_mbps} Mbps")
        rates.append(rate_mbps)

    # compute average
    avg_rate = sum(rates) / len(rates) if rates else 0.0

    return DataTransferRateResponse(
        source=source,
        destination=destination,
        rate_mbps=avg_rate,
        wireless_channel=wireless_channel,
        timestamp=int(datetime.utcnow().timestamp() * 1000)
    )
