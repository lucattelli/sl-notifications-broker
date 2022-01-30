from typing import Dict, Optional
from uuid import UUID, uuid4
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


@dataclass(frozen=True)
class SecondLifeUser:
    second_life_username: str
    second_life_uuid: UUID


@dataclass(frozen=True)
class NotificationMessage:
    body: str


class NotificationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    SUCCESS = "success"


class NotificationInvalidStatus(Exception):
    pass


class Notification:
    def __init__(
        self,
        send_to: SecondLifeUser,
        message: NotificationMessage,
        status: Optional[NotificationStatus] = None,
        notification_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.__send_to = send_to
        self.__message = message
        self.__status: NotificationStatus = status or NotificationStatus.PENDING
        self.__notification_id: UUID = notification_id or uuid4()
        self.__created_at: datetime = created_at or datetime.now()
        self.__updated_at: datetime = updated_at or self.__created_at

    @property
    def status(self) -> NotificationStatus:
        return self.__status

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @property
    def is_pending(self) -> bool:
        return self.__status == NotificationStatus.PENDING

    @property
    def is_successful(self) -> bool:
        return self.__status == NotificationStatus.SUCCESS

    @property
    def is_in_progress(self) -> bool:
        return self.__status == NotificationStatus.IN_PROGRESS

    def set_in_progress(self) -> None:
        if self.__status != NotificationStatus.PENDING:
            raise NotificationInvalidStatus
        self.__set_status(status=NotificationStatus.IN_PROGRESS)

    def set_success(self) -> None:
        self.__assert_in_progress()
        self.__set_status(status=NotificationStatus.SUCCESS)

    def set_failed(self) -> None:
        self.__assert_in_progress()
        self.__set_status(status=NotificationStatus.FAILED)

    def as_dict(self) -> Dict:
        return {
            "send_to": {
                "second_life_uuid": self.__send_to.second_life_uuid,
                "second_life_username": self.__send_to.second_life_username,
            },
            "message": self.__message.body,
            "status": self.__status.value,
            "notification_id": self.__notification_id,
            "created_at": str(self.__created_at),
            "updated_at": str(self.__updated_at),
        }

    def __assert_in_progress(self):
        if not self.is_in_progress:
            raise NotificationInvalidStatus

    def __set_status(self, status: NotificationStatus) -> None:
        self.__status = status
        self.__updated_at = datetime.now()
