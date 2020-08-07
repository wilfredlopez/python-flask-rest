from werkzeug.security import safe_str_cmp
from user import User

wilfred = User(1, 'wilfred', 'password')

users = [wilfred]


username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = User.find_by_username(username=username)
    if user is not None and safe_str_cmp(user.password, password):
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(userId=user_id)
