from utils.db import get_db


def fetch_user_by_email(email):

    db = get_db()

    response = (
        db.table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    return response.data