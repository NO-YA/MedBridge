
from passlib.context import CryptContext

# Prefer Argon2 if available (modern, no 72-byte limit). Fall back to
# bcrypt_sha256 if argon2 is not installed in the environment.
try:
    import argon2  # type: ignore
    _scheme = "argon2"
except Exception:
    # Fall back to a pure-Python PBKDF2 SHA256 when Argon2 isn't available.
    # Using PBKDF2 avoids bcrypt's 72-byte limit and also avoids triggering
    # passlib's bcrypt backend initialization checks on some environments.
    _scheme = "pbkdf2_sha256"

pwd_context = CryptContext(schemes=[_scheme], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt_sha256 (pre-hash + bcrypt).

    This avoids the classic bcrypt 72-byte limit and is the recommended
    way to handle potentially long passphrases.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
