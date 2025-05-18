import base64
from cryptography.fernet import Fernet

def createFernet(key: bytes) -> Fernet:
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt(fernet: Fernet, plaintext: str) -> bytes:
    return fernet.encrypt(plaintext.encode())

def decrypt(fernet: Fernet, token: bytes) -> str:
    return fernet.decrypt(token).decode()