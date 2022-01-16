from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import UUID


class MessageType(Enum):
    COMMAND = "command"
    EVENT = "event"


@dataclass(frozen=True)
class MessageHeader:
    message_id: UUID
    message_type: MessageType
    message_name: str
    created_at: datetime


@dataclass(frozen=True)
class Message:
    message_header: MessageHeader
    message_body: Dict


class MessageBusPort(ABC):
    @abstractmethod
    def publish(self, message: Message) -> None:
        pass
