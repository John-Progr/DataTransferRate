


# Helper functions
def get_channel_frequency(channel: int) -> int:
    """Get frequency for a channel"""
    info = CHANNEL_INFO.get(channel)
    return info["frequency"] if info else None

def get_channel_regions(channel: int) -> tuple:
    """Get regions where this channel is allowed"""
    info = CHANNEL_INFO.get(channel)
    return info["regions"] if info else ()

def is_channel_allowed_in_region(channel: int, region: str) -> bool:
    """Check if channel is allowed in specific region"""
    regions = get_channel_regions(channel)
    return region.upper() in regions

def get_channels_for_region(region: str) -> list:
    """Get all channels allowed in a region"""
    return [channel for channel, info in CHANNEL_INFO.items() 
            if region.upper() in info["regions"]]