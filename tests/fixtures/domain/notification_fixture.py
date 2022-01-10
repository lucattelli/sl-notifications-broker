from typing import Dict, Optional
from uuid import uuid4
from sl_notifications_broker.domain.entities.notification import (
    Notification,
    NotificationMessage,
    SecondLifeUser,
)


def get_notification_fixture(values: Optional[Dict] = None):
    custom_values = values or {}
    send_to = custom_values.get(
        "send_to",
        SecondLifeUser(
            second_life_username="slusername", second_life_uuid=uuid4()
        ),
    )
    message = custom_values.get(
        "message", NotificationMessage(body="This is a custom message")
    )

    return Notification(
        send_to=send_to,
        message=message,
        status=custom_values.get("status"),
        notification_id=custom_values.get("notification_id"),
        created_at=custom_values.get("created_at"),
        updated_at=custom_values.get("updated_at"),
    )
