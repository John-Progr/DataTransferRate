# constants.py
class ThingsConstants:
    """Constants for managing things and their associated IP addresses."""
    
    # Dictionary mapping IP addresses to thing IDs
    IP_TO_THING_ID = {
        "192.168.1.100": "thing_001",
        "192.168.1.101": "thing_002", 
        "192.168.1.102": "thing_003",
        "192.168.1.110": "sensor_hub_01",
        "192.168.1.111": "sensor_hub_02",
        "192.168.1.1": "gateway_main",
        "192.168.1.2": "gateway_backup",
        "10.0.0.50": "controller_alpha",
        "10.0.0.51": "controller_beta",
        "172.16.0.10": "monitor_device",
    }