from auth import (loadConfig, setMasterPassword, verifyMasterPassword, deriveKey)
from crypto_utils import createFernet, encrypt
from crypto_utils import decrypt
from db import init_db, saveEntry, getEntries
import streamlit as st
import os

st.title("🔐 Password Manager")

# Initialize session state for login and setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = os.path.exists("config.json") and loadConfig()["password_hash"] is not None

init_db()

def firstTimeSetup():
    st.write("First-Time Setup: Create a master password")
    password = st.text_input("New Master Password", type="password")
    if st.button("Set Master Password"):
        if password:
            setMasterPassword(password)
            st.success("Master password set! Please refresh the page to log in.")
            st.session_state.setup_complete = True
            st.stop()  # Prevent further code from running
        else:
            st.error("Password cannot be empty")

def login():
    st.write("🔑 Enter your master password")
    password = st.text_input("Master Password", type="password")

    if st.button("Unlock"):
        if not password:
            st.error("Please enter a password")
            st.stop()

        try:
            if verifyMasterPassword(password):
                st.session_state.logged_in = True
                st.session_state.master_password = password
                st.success("Unlocked password manager")
                st.rerun()  # <-- Force Streamlit to rerun script with new state
            else:
                st.error("Incorrect password")
        except Exception as e:
            st.error(f"Error verifying password: {e}")
        st.stop()




def addEntry(fernet):
    service = st.text_input("Service (e.g. Gmail)")
    username = st.text_input("Username/Email")
    pwPlain = st.text_input("Password", type="password")

    if st.button("Save Password"):
        if service and username and pwPlain:
            pwEncrypted = encrypt(fernet, pwPlain)
            saveEntry(service, username, pwEncrypted)
            st.success("Password saved")
        else:
            st.error("All fields are required")

def viewEntry(fernet):
    entries = getEntries()
    if not entries:
        st.info("No entries found.")
        return

    for i, (service, username, pwEncrypted) in enumerate(entries, 1):
        try:
            pwPlain = decrypt(fernet, pwEncrypted)
            st.write(f"**{i}. {service}**\n- User: `{username}`\n- Pass: `{pwPlain}`")
        except Exception:
            st.error(f"{i}. {service} (failed to decrypt)")

def main():
    init_db()

    if not os.path.exists("config.json") or loadConfig()["password_hash"] is None:
        firstTimeSetup()

    elif not st.session_state.logged_in:
        login()

    else:
        password = st.session_state.master_password
        key = deriveKey(password)
        fernet = createFernet(key)

        st.success("✅ Welcome to your password manager!")

        option = st.selectbox("Choose an option", ["Add New Password", "View Stored Passwords"])
        if option == "Add New Password":
            addEntry(fernet)
        elif option == "View Stored Passwords":
            viewEntry(fernet)


if __name__ == "__main__":
    main()
