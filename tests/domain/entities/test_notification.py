from datetime import datetime
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
        self.send_to = SecondLifeUser(
            second_life_username="slusername", second_life_uuid=uuid4()
        )
        self.message = NotificationMessage(
            body="This is a notification message."
        )
        self.notification_id = uuid4()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.notification = Notification(
            send_to=self.send_to,
            message=self.message,
            notification_id=self.notification_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        return super().setUp()

    def test_is_pending_when_status_is_not_pending(self):
        self.notification.set_in_progress()
        expected = False
        actual = self.notification.is_pending
        self.assertEqual(expected, actual)

    def test_is_pending_when_status_is_pending(self):
        expected = True
        actual = self.notification.is_pending
        self.assertEqual(expected, actual)

    def test_is_successful_when_status_is_not_success(self):
        expected = False
        actual = self.notification.is_successful
        self.assertEqual(expected, actual)

    def test_is_successful_when_status_is_success(self):
        self.notification.set_in_progress()
        self.notification.set_success()
        expected = True
        actual = self.notification.is_successful
        self.assertEqual(expected, actual)

    def test_is_in_progress_when_status_is_not_in_progress(self):
        expected = False
        actual = self.notification.is_in_progress
        self.assertEqual(expected, actual)

    def test_is_in_progress_when_status_is_in_progress(self):
        self.notification.set_in_progress()
        expected = True
        actual = self.notification.is_in_progress
        self.assertEqual(expected, actual)

    def test_set_in_progress_when_status_is_pending(self):
        self.notification.set_in_progress()

        self.assertEqual(
            NotificationStatus.IN_PROGRESS, self.notification.status
        )
        self.assertNotEqual(self.updated_at, self.notification.updated_at)

    def test_set_in_progress_when_status_is_not_pending(self):
        self.notification.set_in_progress()
        updated_at = self.notification.updated_at

        with self.assertRaises(NotificationInvalidStatus):
            self.notification.set_in_progress()

        self.assertEqual(
            NotificationStatus.IN_PROGRESS, self.notification.status
        )
        self.assertEqual(updated_at, self.notification.updated_at)

    def test_set_failed_when_status_is_in_progress(self):
        self.notification.set_in_progress()
        self.notification.set_failed()

        self.assertEqual(NotificationStatus.FAILED, self.notification.status)
        self.assertNotEqual(self.updated_at, self.notification.updated_at)

    def test_set_failed_when_status_is_not_in_progress(self):
        with self.assertRaises(NotificationInvalidStatus):
            self.notification.set_failed()

        self.assertEqual(NotificationStatus.PENDING, self.notification.status)
        self.assertEqual(self.updated_at, self.notification.updated_at)

    def test_set_success_when_status_is_in_progress(self):
        self.notification.set_in_progress()
        self.notification.set_success()

        self.assertEqual(NotificationStatus.SUCCESS, self.notification.status)
        self.assertNotEqual(self.updated_at, self.notification.updated_at)

    def test_set_success_when_status_is_not_in_progress(self):
        with self.assertRaises(NotificationInvalidStatus):
            self.notification.set_success()

        self.assertEqual(NotificationStatus.PENDING, self.notification.status)
        self.assertEqual(self.updated_at, self.notification.updated_at)

    def test_as_dict(self):
        expected = {
            "send_to": {
                "second_life_uuid": self.send_to.second_life_uuid,
                "second_life_username": self.send_to.second_life_username,
            },
            "message": self.message.body,
            "status": NotificationStatus.PENDING.value,
            "notification_id": self.notification_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
        actual = self.notification.as_dict()

        self.assertEqual(expected, actual)
