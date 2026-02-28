import bcrypt

def hash_password(password: str) -> str:
    # bcrypt has a 72-byte limit, truncate if necessary
    truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(truncated_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Generate a dummy hash at module load time to be used for mitigating timing attacks
# when a user is not found during authentication.
DUMMY_HASH = hash_password("dummy_password")

def verify_password(password: str, password_hash: str) -> bool:
    # bcrypt has a 72-byte limit, truncate if necessary
    truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return bcrypt.checkpw(truncated_password.encode('utf-8'), password_hash.encode('utf-8'))
