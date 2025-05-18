# Python Based Password Manager

A simple, lightweight password manager built on Python. It was a personal project to build myself a free password manager, but also doubles as a good resume piece.

---

## Features
- Master Password Authentication (Argon-2 Hashed)
- AES encryption using Fernet
- Local SQlite3 for storing passwords
- Session-based login and state mgmt
- All local, no server or cloud use

---

## Tech Stack
- Python 3.10XX
- Streamlit - (Frontend)
- Argon2-cffi (Password hashing)
- Cryptography (Fernet) AES-128 Encryption
- SQLite3 - Data

## How to Use

Simply download the repo, in the editor terminal (VSCode in my case) simply write: streamlit run main.py. This should prompt you to make a master password. If that is successful you'll be able to modify the list of credentials or view the list of credentials.
