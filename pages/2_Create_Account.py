import streamlit as st
import utils.auth as auth

st.title("📝 Créer un compte")

new_username = st.text_input("Nom d'utilisateur")
new_password = st.text_input("Mot de passe", type="password")

if st.button("Créer mon compte"):
    if auth.create_user(new_username, new_password):
        st.success(f"Compte '{new_username}' créé ✅")
        st.switch_page("pages/1_Login.py")
    else:
        st.error("Nom d'utilisateur déjà pris ❌")

if st.button("Retour à la connexion"):
    st.switch_page("pages/1_Login.py")
