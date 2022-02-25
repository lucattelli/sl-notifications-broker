from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from uuid import UUID, uuid4


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
    def id(self) -> UUID:
        return self.__notification_id

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @property
    def message(self) -> NotificationMessage:
        return self.__message

    @property
    def to(self) -> SecondLifeUser:
        return self.__send_to

    @property
    def status(self) -> NotificationStatus:
        return self.__status

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

    @staticmethod
    def from_dict(data: Dict):
        return Notification(
            send_to=SecondLifeUser(
                second_life_username=data["send_to"]["second_life_username"],
                second_life_uuid=data["send_to"]["second_life_uuid"],
            ),
            message=NotificationMessage(body=data["message"]),
            status=NotificationStatus(data["status"])
            if data.get("status")
            else None,
            notification_id=data["notification_id"]
            if data.get("notification_id")
            else None,
            created_at=datetime.strptime(
                data["created_at"], "%Y-%m-%d %H:%M:%S.%f"
            )
            if data.get("created_at")
            else None,
            updated_at=datetime.strptime(
                data["updated_at"], "%Y-%m-%d %H:%M:%S.%f"
            )
            if data.get("updated_at")
            else None,
        )

    def __assert_in_progress(self):
        if not self.is_in_progress:
            raise NotificationInvalidStatus

    def __set_status(self, status: NotificationStatus) -> None:
        self.__status = status
        self.__updated_at = datetime.now()


    def __eq__(self, other) -> bool:
        return self.id == other.id
