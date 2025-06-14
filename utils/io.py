import json
import os
from models import DataTransferRateResponse


def save_data_transfer_rate_to_file(
    response: DataTransferRateResponse,
    file_path: str = "data_transfer_log.json"
):
    if not response.timestamp:
        from datetime import datetime
        response.timestamp = datetime.utcnow().isoformat()

    record = response.dict()

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(record)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
