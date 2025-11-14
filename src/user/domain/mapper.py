"""Mapper functions for User domain model."""

from src.database import database
from src.user.domain import model


def userdoc_to_domain(user_doc: database.UserDoc, devices: list[database.DeviceDoc] | None = None) -> model.User:
    """Map UserDoc to User domain model."""
    return model.User(
        id=str(user_doc.id),
        fullname=user_doc.fullname,
        devices=[device.device_id for device in devices] if devices else [],
    )
