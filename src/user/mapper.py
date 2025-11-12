from src.database import database
from src.user import model


def userdoc_to_domain(user_doc: database.UserDoc, devices: list[database.DeviceDoc] | None = None) -> model.User:
    return model.User(
        fullname=user_doc.fullname,
        devices=[device.device_id for device in devices] if devices else [],
    )