from src.database import database
from src.user import model


def userdoc_to_domain(user_doc: database.UserDoc, device_ids: list[str] | None = None) -> model.User:
    return model.User(
        fullname=user_doc.fullname,
        devices=device_ids or [],
    )