import streamlit as st
import utils.auth as auth

st.title("🔑 Connexion")

username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    if auth.verify_user(username, password):  # Vérification dans auth.py
        st.success("Connexion réussie ✅")
        st.switch_page("pages/3_Finances.py")
    else:
        st.error("Identifiants incorrects ❌")

if st.button("Créer un compte"):
    st.switch_page("pages/2_Create_Account.py")
