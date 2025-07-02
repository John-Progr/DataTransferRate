from datetime import datetime
from models import DataTransferRateResponse



def get_data_transfer_rate(source: str, destination: str, path: List[str], wireless_channel: Optional[int]) -> DataTransferRateResponse:
   
   #take the inputs and started distributing the messages to the appropriate nodes
   # WE 've got the wireless channel but we need to check the region that is avaliable!
   regions = get_regiona(wireless_channel) 
   # This will return a tuple we pick the first one 
   region = get_region(regions)
   # The first to send is the server one so it can start running 
   destination_id = get_thing_id_by_ip(destination)
   
   payload_destination = {
    "role": "server",
    "wireless_channel": wireless_channel,
    "region": region,
    "ip_routing": null
   }

   await send_message_to_ditto(payload_destination,destination_id)

   #if ok then send ok ( we ll search on this)
   
  #here we will run a loop for each intermdiate node from path list 

  for intermediate_node in filter(None, path):
    intermediate_id = get_thing_id_by_ip(intermediate_node)
    
    payload_intermediate = {
        "role": "intermediate",
        "wireless_channel": wireless_channel,
        "region": region

    }

    await send_message_to_ditto(payload_intermediate, intermediate_id)

   #we start by sending the iperf client the role:client,the channel: wireless_channel 
   payload_source = {
    "role": "client",
    "wireless_channel": wireless_channel,
    "region": region
   }

   source_id = get_thing_id_by_ip(source)

   await send_message_to_ditto(payload_source, source_id)

   async for state in get_digital_twin_state():
    
    if thing_id = state,get(source_id):
        #something similar
        neighbors = state.get("features", {}).get("network", {}).get("properties", {}).get("neighbors", [])
        break
    

    return DataTransferRateResponse(
        source=source,
        destination=destination,
        rate_mbps=rate_mbps,
        wireless_channel = wireless_channel,
        timestamp=datetime.utcnow().isoformat()
    )
