def load_credentials():
    """Hardcoded admin credentials."""
    return {"admin": "admin"}

def verify_credentials(username, password):
    """Verify against hardcoded admin/admin."""
    return username == "admin" and password == "admin"
