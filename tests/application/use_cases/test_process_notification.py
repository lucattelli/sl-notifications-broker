from copy import deepcopy
from unittest import TestCase
from unittest.mock import Mock

from sl_notifications_broker.application.ports.notification_repository_port import (
    NotificationRepositoryPort,
)
from sl_notifications_broker.application.ports.worker_interface_port import (
    WorkerCommunicationFailure,
    WorkerInterfacePort,
)
from sl_notifications_broker.application.ports.worker_repository_port import (
    WorkerNotFound,
    WorkerRepositoryPort,
)
from sl_notifications_broker.application.use_cases.process_notification import (
    ProcessNotification,
)
from sl_notifications_broker.domain.entities.notification import (
    NotificationInvalidStatus,
    NotificationStatus,
)
from tests.fixtures.domain.notification_fixture import get_notification_fixture
from tests.fixtures.domain.worker_fixture import get_worker_fixture


class TestProcessNotification(TestCase):
    def setUp(self) -> None:
        self.notification_fixture = get_notification_fixture()
        self.worker_fixture = get_worker_fixture()

        self.worker_repository_mock = Mock(spec=WorkerRepositoryPort)
        self.worker_repository_mock.get_all.return_value = [self.worker_fixture]

        self.worker_interface_mock = Mock(spec=WorkerInterfacePort)
        self.notification_repository_mock = Mock(
            spec=NotificationRepositoryPort
        )
        self.process_notification = ProcessNotification(
            worker_repository=self.worker_repository_mock,
            worker_interface=self.worker_interface_mock,
            notification_repository=self.notification_repository_mock,
        )
        super().setUp()

    def tearDown(self) -> None:
        self.worker_repository_mock.reset_mock()
        self.worker_interface_mock.reset_mock()
        self.notification_repository_mock.reset_mock()
        super().tearDown()

    def test_call_when_notification_status_is_not_pending(self):
        self.notification_fixture.set_in_progress()
        with self.assertRaises(NotificationInvalidStatus):
            self.process_notification(notification=self.notification_fixture)

    def test_call_when_no_worker_is_found(self):
        self.worker_repository_mock.get_all.return_value = []
        with self.assertRaises(WorkerNotFound):
            self.process_notification(notification=self.notification_fixture)

    def test_call_when_all_worker_fails_to_process_notification(self):
        expected = NotificationStatus.FAILED

        self.worker_interface_mock.process_notification.side_effect = (
            WorkerCommunicationFailure
        )
        self.process_notification(notification=self.notification_fixture)

        actual = self.notification_repository_mock.update.call_args_list[-1][1][
            "notification"
        ].status

        self.assertEqual(expected, actual)

    def test_call_when_worker_succeeds_to_process_notification(self):
        expected = NotificationStatus.SUCCESS

        self.process_notification(notification=self.notification_fixture)

        actual = self.notification_repository_mock.update.call_args_list[-1][1][
            "notification"
        ].status

        self.assertEqual(expected, actual)
