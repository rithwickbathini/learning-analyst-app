"""Authentication service functions."""

from utils.db import get_db


def get_user_by_email(email):

    db = get_db()

    if db is None:
        return None

    try:
        response = (
            db.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )

        if response.data:
            return response.data[0]

        return None

    except Exception:
        return None