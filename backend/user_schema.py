user_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_]{3,32}$"
        },
        "password": {
            "type": "string",
            "minLength": 6,
            "pattern": "^(?=.*[A-Za-z])(?=.*\\d).+$"
        }
    },
    "required": ["username", "password"]
}

def get_user_schema():
    return user_schema 