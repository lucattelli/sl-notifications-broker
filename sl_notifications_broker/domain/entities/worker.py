from typing import Dict, Optional
from uuid import UUID
from enum import Enum
from datetime import datetime


class WorkerStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class Worker:
    def __init__(
        self,
        worker_uuid: UUID,
        worker_status: WorkerStatus,
        worker_url: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.__worker_uuid = worker_uuid
        self.__worker_status = worker_status
        self.__worker_url = worker_url
        self.__created_at: datetime = created_at or datetime.now()
        self.__updated_at: datetime = updated_at or self.__created_at

    def as_dict(self) -> Dict:
        return {
            "worker_uuid": self.__worker_uuid,
            "worker_status": self.__worker_status.value,
            "worker_url": self.__worker_url,
            "created_at": str(self.__created_at),
            "updated_at": str(self.__updated_at),
        }

    def heartbeat(self) -> None:
        self.__updated_at = datetime.now()
