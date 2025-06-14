from datetime import datetime
from models import DataTransferRateResponse


def get_data_transfer_rate(source: str, destination: str) -> DataTransferRateResponse:
    # Placeholder logic. Replace this with actual logic (e.g., from a database or calculation)
    rate_mbps = 100.0  # Dummy value

    return DataTransferRateResponse(
        source=source,
        destination=destination,
        rate_mbps=rate_mbps,
        timestamp=datetime.utcnow().isoformat()
    )
