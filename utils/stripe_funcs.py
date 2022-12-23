import hashlib
import secrets


def generate_api_key(key_length=32):
    # Generate a new API key using the secrets module
    api_key = secrets.token_hex(key_length)
    return api_key


def hash_api_key(api_key):
    # Hash the API key using SHA-256
    hashed_api_key = hashlib.sha256(api_key.encode()).hexdigest()
    return hashed_api_key


def unhash_api_key(hashed_api_key, api_key):
    # Re-hash the provided API key and compare it to the hashed API key
    if hash_api_key(api_key) == hashed_api_key:
        return api_key
    else:
        return None
