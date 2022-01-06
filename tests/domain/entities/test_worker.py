from datetime import datetime
from unittest import TestCase
from uuid import uuid4

from sl_notifications_broker.domain.entities.worker import Worker, WorkerStatus


class TestWorker(TestCase):
    def setUp(self) -> None:
        self.worker_uuid = uuid4()
        self.worker_status = WorkerStatus.ONLINE
        self.worker_url = "https://slworkerurl.com"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.worker = Worker(
            worker_uuid=self.worker_uuid,
            worker_status=self.worker_status,
            worker_url=self.worker_url,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        super().setUp()

    def test_as_dict(self):
        expected = {
            "worker_uuid": self.worker_uuid,
            "worker_status": self.worker_status.value,
            "worker_url": self.worker_url,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }

        actual = self.worker.as_dict()

        self.assertEqual(expected, actual)

    def test_heartbeat(self):
        self.worker.heartbeat()

        data = self.worker.as_dict()

        self.assertNotEqual(str(self.updated_at), data["updated_at"])
