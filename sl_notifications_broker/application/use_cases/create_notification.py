from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from uuid import UUID, uuid4
from enum import Enum
from sl_notifications_broker.domain.entities.notification import Notification


class NotificationRepositoryPort(ABC):
    @abstractmethod
    def insert(self, notification: Notification) -> None:
        pass


class MessageType(Enum):
    COMMAND = "command"
    EVENT = "event"


@dataclass(frozen=True)
class MessageHeader:
    message_id: UUID
    message_type: MessageType
    message_name: str
    created_at: datetime


@dataclass(frozen=True)
class Message:
    message_header: MessageHeader
    message_body: Dict


class MessageBusPort(ABC):
    @abstractmethod
    def publish(self, message: Message) -> None:
        pass


@dataclass(frozen=True)
class SecondLifeNotificationCreatedEvent(Message):
    @staticmethod
    def factory(
        notification: Notification,
    ):
        return SecondLifeNotificationCreatedEvent(
            message_header=MessageHeader(
                message_id=uuid4(),
                message_type=MessageType.EVENT,
                message_name="second_life_notification_created",
                created_at=datetime.now(),
            ),
            message_body=notification.as_dict(),
        )


class CreateNotification:
    def __init__(
        self,
        notification_repository: NotificationRepositoryPort,
        message_bus: MessageBusPort,
    ):
        self.__notification_repository = notification_repository
        self.__message_bus = message_bus

    def __call__(self, notification: Notification) -> None:
        self.__notification_repository.insert(notification=notification)
        self.__message_bus.publish(
            message=SecondLifeNotificationCreatedEvent.factory(
                notification=notification
            )
        )
