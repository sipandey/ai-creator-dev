import bcrypt

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

# Generate a dummy hash at module level for timing attack mitigation
# This ensures that non-existent user lookups take roughly the same time as existing ones
DUMMY_HASH = hash_password("dummy_password_for_timing_mitigation")
