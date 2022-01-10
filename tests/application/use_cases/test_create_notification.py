from unittest import TestCase
from unittest.mock import Mock

from sl_notifications_broker.application.use_cases.create_notification import (
    CreateNotification,
    SecondLifeNotificationCreatedEvent,
)
from tests.fixtures.domain.notification_fixture import get_notification_fixture


class TestCreateNotification(TestCase):
    def setUp(self) -> None:
        self.notification = get_notification_fixture()

        self.notification_repository_mock = Mock()
        self.message_bus_mock = Mock()
        self.event_factory_mock = Mock()
        self.notification_created_event = (
            SecondLifeNotificationCreatedEvent.factory(
                notification=self.notification
            )
        )
        self.event_factory_mock.notification_created_factory.return_value = (
            self.notification_created_event
        )

        self.create_notification = CreateNotification(
            notification_repository=self.notification_repository_mock,
            message_bus=self.message_bus_mock,
            event_factory=self.event_factory_mock,
        )
        super().setUp()

    def tearDown(self) -> None:
        self.notification_repository_mock.reset_mock()
        self.message_bus_mock.reset_mock()
        super().tearDown()

    def test_call_when_save_succeeds(self):
        self.create_notification(notification=self.notification)

        self.notification_repository_mock.insert.assert_called_once_with(
            notification=self.notification
        )

        self.event_factory_mock.notification_created_factory.assert_called_once_with(
            notification=self.notification
        )

        self.message_bus_mock.publish.assert_called_once_with(
            message=self.notification_created_event
        )

    def test_call_when_save_fails(self):
        self.notification_repository_mock.insert.side_effect = Exception

        with self.assertRaises(Exception):
            self.create_notification(notification=self.notification)

        self.notification_repository_mock.insert.assert_called_once_with(
            notification=self.notification
        )

        self.event_factory_mock.notification_created_factory.assert_not_called()

        self.message_bus_mock.publish.assert_not_called()
