import streamlit as st
import json
import firebase_admin
from firebase_admin import db
import utils.accounts as accounts

st.title("📝 Créer un compte")

new_username = st.text_input("Nom d'utilisateur")
new_password = st.text_input("Mot de passe", type="password")

def get_users():
    """Récupère tous les utilisateurs depuis Firebase."""
    ref = db.reference("users")
    return ref.get() or {}  # Retourne un dict vide si aucun utilisateur

def create_user(username, password):
    """Ajoute un nouvel utilisateur à Firebase."""
    users = get_users()
    if username in users:
        return False  # Nom déjà pris
    db.reference(f"users/{username}").set({"password": password})
    return True

if st.button("Créer mon compte"):
    if new_username and new_password:
        if create_user(new_username, new_password):
            new_account = accounts.App_Account(new_username)
            st.success(f"Compte '{new_username}' créé ✅")
            st.session_state["new_user_created"] = True
            st.rerun()
        else:
            st.error("Nom d'utilisateur déjà pris ❌")
    else:
        st.error("Veuillez remplir tous les champs.")

# Redirection après création
if "new_user_created" in st.session_state and st.session_state["new_user_created"]:
    st.switch_page("pages/1_Login.py")

if st.button("Retour à la connexion"):
    st.switch_page("pages/1_Login.py")
