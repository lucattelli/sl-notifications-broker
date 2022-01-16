from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from sl_notifications_broker.domain.ports.message_bus_port import (
    Message,
    MessageHeader,
    MessageType,
)
from sl_notifications_broker.domain.entities.notification import Notification


@dataclass(frozen=True)
class NotificationCreatedEvent(Message):
    @staticmethod
    def factory(
        notification: Notification,
    ):
        return NotificationCreatedEvent(
            message_header=MessageHeader(
                message_id=uuid4(),
                message_type=MessageType.EVENT,
                message_name="second_life_notification_created",
                created_at=datetime.now(),
            ),
            message_body=notification.as_dict(),
        )
