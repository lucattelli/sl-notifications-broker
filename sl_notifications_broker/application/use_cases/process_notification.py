import logging
from copy import deepcopy
from typing import List

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
from sl_notifications_broker.domain.entities.notification import (
    Notification,
    NotificationInvalidStatus,
)
from sl_notifications_broker.domain.entities.worker import Worker


class ProcessNotification:
    def __init__(
        self,
        worker_repository: WorkerRepositoryPort,
        worker_interface: WorkerInterfacePort,
        notification_repository: NotificationRepositoryPort,
    ) -> None:
        self.__worker_repository = worker_repository
        self.__worker_interface = worker_interface
        self.__notification_repository = notification_repository
        self.__logger = logging.getLogger()

    def __call__(self, notification: Notification) -> None:
        self.__assert_notification_is_pending(notification=notification)
        self.__process_notification(notification=notification)

    @staticmethod
    def __assert_notification_is_pending(notification: Notification) -> None:
        if not notification.is_pending:
            raise NotificationInvalidStatus

    def __update_notification(self, notification: Notification) -> None:
        self.__notification_repository.update(notification=notification)
        # TODO: Publish NotificationUpdatedEvent

    def __get_all_workers(self) -> List[Worker]:
        workers = self.__worker_repository.get_all()
        if not workers:
            raise WorkerNotFound
        return workers

    def __process_notification(
        self, notification: Notification
    ) -> Notification:
        notification_to_process = deepcopy(notification)
        notification_to_process.set_in_progress()
        self.__update_notification(notification=notification_to_process)

        workers = self.__get_all_workers()
        for worker in workers:
            try:
                self.__worker_interface.process_notification(
                    worker=worker,
                    notification=notification_to_process,
                )
                notification_to_process.set_success()
                self.__notification_repository.update(
                    notification=notification_to_process
                )
                self.__logger.debug(
                    "Notification %s processed by worker %s with success.",
                    str(notification_to_process),
                    str(worker),
                )
                break
            except WorkerCommunicationFailure:
                pass

        if notification_to_process.is_in_progress:
            notification_to_process.set_failed()
            self.__update_notification(notification=notification_to_process)
            self.__logger.error(
                "Failed to process notification %s.",
                str(notification_to_process),
            )
