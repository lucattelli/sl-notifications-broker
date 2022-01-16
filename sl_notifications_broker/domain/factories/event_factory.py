from sl_notifications_broker.domain.entities.notification import Notification
from sl_notifications_broker.domain.events.notification_created_event import (
    NotificationCreatedEvent,
)


class EventFactory:
    @staticmethod
    def notification_created_factory(
        notification: Notification,
    ) -> NotificationCreatedEvent:
        return NotificationCreatedEvent.factory(notification=notification)
