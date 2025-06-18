from flask import session, redirect, url_for
from functools import wraps
from models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if "user_id" in session:
        return User.get_by_id(session["user_id"])
    return None
