import streamlit as st
import firebase_admin
from firebase_admin import db



# Référence à la base de données
users_ref = db.reference("users")

def verify_user(username, password):
    """ Vérifie si l'utilisateur existe et si le mot de passe correspond """
    user_data = users_ref.child(username).get()
    return user_data is not None and user_data.get("password") == password

def create_user(username, password):
    """ Crée un nouvel utilisateur s'il n'existe pas déjà """
    if users_ref.child(username).get():
        return False  # L'utilisateur existe déjà
    
    users_ref.child(username).set({"password": password})
    return True
