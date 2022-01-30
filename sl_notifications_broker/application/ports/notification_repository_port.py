from abc import ABC, abstractmethod

from sl_notifications_broker.domain.entities.notification import Notification


class NotificationRepositoryPort(ABC):
    @abstractmethod
    def insert(self, notification: Notification) -> None:
        pass

    @abstractmethod
    def update(self, notification: Notification) -> None:
        pass
