import streamlit as st
import utils.auth as auth
import json
import os

st.title("📝 Créer un compte")

new_username = st.text_input("Nom d'utilisateur")
new_password = st.text_input("Mot de passe", type="password")

# Charger les données existantes ou créer un fichier vide
data_file = "data.json"

if os.path.exists(data_file):
    with open(data_file, "r") as f:
        try:
            account_data = json.load(f)
        except json.JSONDecodeError:
            account_data = {}  # Fichier vide ou corrompu
else:
    account_data = {}

if st.button("Créer mon compte"):
    if new_username in account_data:
        st.error("Nom d'utilisateur déjà pris ❌")
    elif new_username and new_password:
        # Ajouter le nouvel utilisateur
        account_data[new_username] = new_password
        with open(data_file, "w") as f:
            json.dump(account_data, f, indent=4)  # Sauvegarde du fichier JSON

        st.success(f"Compte '{new_username}' créé ✅")

        # Redirection après création du compte
        st.session_state["new_user_created"] = True
        st.rerun()
    else:
        st.error("Veuillez remplir tous les champs.")

# Redirection après création
if "new_user_created" in st.session_state and st.session_state["new_user_created"]:
    st.switch_page("pages/1_Login.py")

if st.button("Retour à la connexion"):
    st.switch_page("pages/1_Login.py")
