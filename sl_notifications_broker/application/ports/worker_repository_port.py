from abc import ABC, abstractmethod
from typing import List

from sl_notifications_broker.domain.entities.worker import Worker


class WorkerNotFound(Exception):
    pass


class WorkerRepositoryPort(ABC):
    @abstractmethod
    def get_all(self) -> List[Worker]:
        pass
