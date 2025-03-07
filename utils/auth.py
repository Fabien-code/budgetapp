import streamlit as st

USERS_DB = {"admin": "admin"}  # Exemple basique

def verify_user(username, password):
    return USERS_DB.get(username) == password

def create_user(username, password):
    if username in USERS_DB:
        return False
    USERS_DB[username] = password
    return True
