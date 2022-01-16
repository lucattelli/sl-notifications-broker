from sl_notifications_broker.domain.factories.event_factory import EventFactory
from sl_notifications_broker.domain.ports.message_bus_port import (
    MessageBusPort,
)
from sl_notifications_broker.application.ports.notification_repository_port import (
    NotificationRepositoryPort,
)
from sl_notifications_broker.domain.entities.notification import Notification


class CreateNotification:
    def __init__(
        self,
        notification_repository: NotificationRepositoryPort,
        message_bus: MessageBusPort,
        event_factory: EventFactory,
    ):
        self.__notification_repository = notification_repository
        self.__message_bus = message_bus
        self.__event_factory = event_factory

    def __call__(self, notification: Notification) -> None:
        self.__notification_repository.insert(notification=notification)

        event = self.__event_factory.notification_created_factory(
            notification=notification
        )
        self.__message_bus.publish(message=event)
