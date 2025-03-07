import json
import os
import streamlit as st

# Charger les données existantes ou créer un fichier vide
data_file = "data.json"

if os.path.exists(data_file):
    with open(data_file, "r") as f:
        try:
            account_data = json.load(f)
        except json.JSONDecodeError:
            account_data = {}  # Fichier vide ou corrompu

def verify_user(username, password):
    print(account_data.get(username), password)
    return account_data.get(username) == password

def create_user(username, password):
    if username in account_data:
        print("User already exists", account_data)
        return False
    
    account_data[username] = password
    return True
