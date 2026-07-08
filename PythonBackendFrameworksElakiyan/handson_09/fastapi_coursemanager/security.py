from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

# bcrypt's work factor makes brute-force attacks computationally expensive -
# each guess takes real time. MD5/SHA-256 are designed to hash FAST, which is
# exactly the wrong property for passwords: an attacker can try billions of
# guesses per second against a leaked SHA-256 hash table.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'dev-jwt-secret-change-in-production'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
