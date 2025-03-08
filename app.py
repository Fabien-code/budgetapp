import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import os

st.set_page_config(page_title="Budget App", layout="wide")

st.title("🏠 Bienvenue sur l'application Budget")

st.sidebar.success("Sélectionnez une page ci-dessus.")



if not firebase_admin._apps:
    # Initialisation de Firebase avec la clé privée
    firebase_key = st.secrets["FIREBASE_KEY"]
    dictionnaire_destination = {}

    # Parcourir chaque élément du dictionnaire source
    for key, value in firebase_key.items():
        # Ajouter chaque clé, valeur dans le dictionnaire destination
        dictionnaire_destination[key] = value
    with open("firebase_key.json", 'w') as f:
        json.dump(dictionnaire_destination, f, indent=4)
    cred = credentials.Certificate("firebase_key.json")  # Chemin vers ta clé
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://budgetdb-13a11-default-rtdb.europe-west1.firebasedatabase.app"  # Remplace par ton URL Firebase
    })
    os.remove("firebase_key.json")
    st.balloons()