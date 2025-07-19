# mqtt_dependencies.py
import logging
from typing import Dict
from fastapi import Depends, HTTPException
from mqtt_core.mqtt_client import MQTTClient

logger = logging.getLogger(__name__)

# Global MQTT client instance
mqtt_client = MQTTClient()

def get_mqtt_client() -> MQTTClient:
    """
    FastAPI dependency function to get the MQTT client.
    Ensures connection is active before returning client.
    """
    if not mqtt_client.ensure_connection():
        logger.error("MQTT client connection failed")
        raise HTTPException(
            status_code=503, 
            detail="MQTT service unavailable - cannot connect to broker"
        )
    return mqtt_client

async def startup_mqtt():
    """
    Initialize MQTT connection on application startup.
    Call this in your FastAPI app startup event.
    """
    logger.info("Starting MQTT client...")
    if not mqtt_client.connect():
        raise Exception("Failed to initialize MQTT connection on startup")
    
    # Add default message handlers for device responses
    def handle_device_response(topic: str, payload: Dict):
        """Handle responses from Raspberry Pi devices"""
        logger.info(f"Device response on {topic}: {payload}")
        # You can add more sophisticated handling here
        # e.g., update database, notify websockets, etc.
    
    def handle_device_status(topic: str, payload: Dict):
        """Handle device status updates"""
        logger.info(f"Device status update on {topic}: {payload}")
        # Handle status updates from devices
    
    # Register message handlers
    mqtt_client.add_message_handler("response/+/+", handle_device_response)
    mqtt_client.add_message_handler("status/+", handle_device_status)
    
    logger.info("MQTT client started successfully")

async def shutdown_mqtt():
    """
    Clean up MQTT connection on application shutdown.
    Call this in your FastAPI app shutdown event.
    """
    logger.info("Shutting down MQTT client...")
    mqtt_client.disconnect()
    logger.info("MQTT client shutdown complete")

def get_mqtt_status() -> Dict:
    """
    Get current MQTT connection status.
    Useful for health checks and monitoring.
    """
    return mqtt_client.get_status()