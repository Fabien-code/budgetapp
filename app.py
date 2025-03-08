import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.set_page_config(page_title="Budget App", layout="wide")

st.title("🏠 Bienvenue sur l'application Budget")

st.sidebar.success("Sélectionnez une page ci-dessus.")


if not firebase_admin._apps:
    # Initialisation de Firebase avec la clé privée
    cred = credentials.Certificate("firebase_key.json")  # Chemin vers ta clé
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://budgetdb-13a11-default-rtdb.europe-west1.firebasedatabase.app"  # Remplace par ton URL Firebase
    })

    st.balloons()