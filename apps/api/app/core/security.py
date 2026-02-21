import bcrypt

# Generate a dummy hash at startup for timing attack mitigation
# This ensures that invalid login attempts take roughly the same amount of time as valid ones
DUMMY_HASH = bcrypt.hashpw(b"dummy_password", bcrypt.gensalt()).decode('utf-8')

def hash_password(password: str) -> str:
    # bcrypt has a 72-byte limit, truncate if necessary
    truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(truncated_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    # bcrypt has a 72-byte limit, truncate if necessary
    truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return bcrypt.checkpw(truncated_password.encode('utf-8'), password_hash.encode('utf-8'))
