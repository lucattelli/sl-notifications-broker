from unittest import TestCase
from uuid import uuid4

from sl_notifications_broker.domain.entities.notification import (
    Notification,
    NotificationInvalidStatus,
    NotificationMessage,
    NotificationStatus,
    SecondLifeUser,
)


class TestNotification(TestCase):
    def setUp(self) -> None:
        self.notification = Notification(
            send_to=SecondLifeUser(
                second_life_username="slusername", second_life_uuid=uuid4()
            ),
            message=NotificationMessage(body="This is a notification message."),
        )
        return super().setUp()

    def test_set_in_progress_when_status_is_pending(self):
        self.notification.set_in_progress()

        self.assertEqual(
            NotificationStatus.IN_PROGRESS, self.notification.status
        )

    def test_set_in_progress_when_status_is_not_pending(self):
        self.notification.set_in_progress()

        with self.assertRaises(NotificationInvalidStatus):
            self.notification.set_in_progress()

    def test_set_failed_when_status_is_in_progress(self):
        self.notification.set_in_progress()
        self.notification.set_failed()

        self.assertEqual(NotificationStatus.FAILED, self.notification.status)

    def test_set_failed_when_status_is_not_in_progress(self):
        with self.assertRaises(NotificationInvalidStatus):
            self.notification.set_failed()

    def test_set_success_when_status_is_in_progress(self):
        self.notification.set_in_progress()
        self.notification.set_success()

        self.assertEqual(NotificationStatus.SUCCESS, self.notification.status)

    def test_set_success_when_status_is_not_in_progress(self):
        with self.assertRaises(NotificationInvalidStatus):
            self.notification.set_success()
