import os
import json
from argon2 import PasswordHasher
from argon2.low_level import hash_secret_raw, Type

configFile = "config.json"

def loadConfig():
    with open(configFile, "r") as f:
        return json.load(f)

def saveConfig(data):
    with open(configFile, "w") as f:
        json.dump(data, f)

def setMasterPassword(password: str):
    salt = os.urandom(16)
    ph = PasswordHasher()
    passwordHash = ph.hash(password)

    config = {
        "salt": salt.hex(),
        "password_hash": passwordHash
    }
    saveConfig(config)

def verifyMasterPassword(password: str):
    if password is None:
        raise ValueError("Password is None")

    config = loadConfig()
    stored_hash = config.get("password_hash")

    if stored_hash is None:
        raise ValueError("No password hash stored in config file")

    ph = PasswordHasher()
    return ph.verify(stored_hash, password)

def deriveKey(password: str) -> bytes:
    config = loadConfig()
    salt = bytes.fromhex(config["salt"])
    key = hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=2,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        type=Type.ID
    )
    return key
