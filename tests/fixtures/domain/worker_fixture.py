from typing import Dict, Optional
from uuid import uuid4

from sl_notifications_broker.domain.entities.worker import Worker, WorkerStatus


def get_worker_fixture(values: Optional[Dict] = None):
    custom_values = values or {}
    return Worker(
        worker_uuid=custom_values.get("worker_uuid", uuid4()),
        worker_status=custom_values.get("worker_status", WorkerStatus.ONLINE),
        worker_url=custom_values.get(
            "worker_url", "https://lslurlforworker.com"
        ),
        created_at=custom_values.get("created_at"),
        updated_at=custom_values.get("updated_at"),
    )
