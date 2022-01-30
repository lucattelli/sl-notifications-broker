from abc import ABC, abstractmethod

from sl_notifications_broker.domain.entities.notification import Notification
from sl_notifications_broker.domain.entities.worker import Worker


class WorkerCommunicationFailure(Exception):
    pass


class WorkerInterfacePort(ABC):
    @abstractmethod
    def process_notification(
        self,
        worker: Worker,
        notification: Notification,
    ) -> None:
        pass
