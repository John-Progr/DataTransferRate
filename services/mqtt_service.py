# mqtt_service.py
import logging
from typing import Dict, Any, Union
from mqtt_core.mqtt_client import MQTTClient
from models.mqtt_model import ClientCommand, ForwarderCommand, ServerCommand


logger = logging.getLogger(__name__)

class MQTTService:
    """Service layer for sending commands to Raspberry Pi devices via MQTT."""
    
    def __init__(self, mqtt_client: MQTTClient):
        self.mqtt_client = mqtt_client
        self.latest_telemetry: Optional[Dict[str, Any]] = None  




    
        
    def subscribe_to_telemetry(self) -> bool:
        """Subscribe to the 'telemetry' topic."""
        return self.mqtt_client.subscribe_to_pi_topic("telemetry")

    
    def get_latest_telemetry(self) -> Optional[Dict[str, Any]]:
        """Return the most recent telemetry data received."""
        return self.latest_telemetry

    

    def send_command(self, cmd: Union[ClientCommand, ForwarderCommand, ServerCommand]) -> Dict[str, Any]:
        """Send any type of command to a Raspberry Pi."""
        try:
            # Build payload based on command type
            if isinstance(cmd, ClientCommand):
                payload = {
                    "role": "client",
                    "wireless_channel": cmd.wireless_channel,
                    "region": cmd.region,
                    "ip_server": cmd.ip_server,
                    "ip_routing": cmd.ip_routing,
                }
            elif isinstance(cmd, ForwarderCommand):
                payload = {
                    "role": "intermediate",
                    "wireless_channel": cmd.wireless_channel,
                    "region": cmd.region,
                    "ip_routing": cmd.ip_routing,
                }
            elif isinstance(cmd, ServerCommand):
                payload = {
                    "role": "server",
                    "wireless_channel": cmd.wireless_channel,
                    "region": cmd.region,
                    "ip_routing": None,
                }
            else:
                return {"status": "error", "message": "Unknown command type"}
            
            # Send the command
            success = self.mqtt_client.send_command_to_pi(cmd.device_id, payload)
            
            if success:
                return {
                    "status": "success",
                    "device_id": cmd.device_id,
                    "role": payload["role"]
                }
            else:
                return {
                    "status": "error",
                    "device_id": cmd.device_id,
                    "message": "Failed to send command"
                }
                
        except Exception as e:
            logger.error(f"Error sending command to {cmd.device_id}: {e}")
            return {
                "status": "error",
                "device_id": cmd.device_id,
                "message": str(e)
            }
    

    def receive_results(self, topic: str, payload: Dict[str, Any]):
        """Callback for MQTT messages."""
        logger.info(f"[MQTTService] Incoming message on topic '{topic}': {payload}")

        if topic == "telemetry":
            # Save the latest telemetry payload
            self.latest_telemetry = payload
            logger.info("[MQTTService] Telemetry updated")
            return self.latest_telemetry

        else:
            logger.warning(f"[MQTTService] Unhandled topic '{topic}'")





    def send_network_setup(self, server_cmd: ServerCommand, 
                          forwarder_cmds: list[ForwarderCommand], 
                          client_cmd: ClientCommand) -> Dict[str, Any]:
        """Send complete network setup commands in correct order."""
        results = []
        
        # Send server first
        results.append(self.send_command(server_cmd))
        
        # Send forwarders
        for forwarder_cmd in forwarder_cmds:
            results.append(self.send_command(forwarder_cmd))
        
        # Send client last
        results.append(self.send_command(client_cmd))
        
        # Check overall status
        failed = [r for r in results if r["status"] != "success"]
        
        return {
            "overall_status": "success" if not failed else "partial_failure" if len(failed) < len(results) else "failure",
            "results": results,
            "failed_count": len(failed)
        }


# Factory function
def create_mqtt_service(mqtt_client: MQTTClient) -> MQTTService:
    return MQTTService(mqtt_client)