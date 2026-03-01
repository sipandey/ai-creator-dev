import bcrypt

# Generate dummy hash at import time to ensure constant-time auth check
# when the user is not found, preventing user enumeration attacks.
# We encode dummy to utf-8 as bcrypt requires bytes.
DUMMY_HASH = bcrypt.hashpw(b'dummy_password', bcrypt.gensalt()).decode('utf-8')

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
