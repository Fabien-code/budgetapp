import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from script.Classes import App_Account

# Simuler une base d’utilisateurs (à remplacer par une vraie base de données)
USERS = {"admin": "password123", "user": "testpass"}

# Initialisation de l'état de session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "finances" not in st.session_state:
    st.session_state.finances = App_Account(name="Finances")

finances = st.session_state.finances  # Récupération de l'instance

# ----------------------------- PAGE DE CONNEXION -----------------------------
def login_page():
    st.title("🔐 Connexion")
    
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Connexion réussie ✅")
            st.rerun()  # Recharger la page
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect ❌")

# ------------------------ PAGE DE GESTION DES COMPTES ------------------------
def account_page():
    st.sidebar.title(f"👤 Connecté en tant que {st.session_state.username}")
    if st.sidebar.button("🔴 Déconnexion"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()

    st.title("💰 Gestion de Comptes Financiers")

    # Section création de compte
    st.header("🔹 Création de compte")
    account_name = st.text_input("Nom du compte à créer")
    if st.button("Créer un compte"):
        if account_name:
            finances.create_account(account_name)
            st.success(f"Compte '{account_name}' créé avec succès!")
        else:
            st.error("Veuillez entrer un nom de compte valide.")

    # Affichage des comptes existants
    st.header("📜 Comptes existants")
    accounts = finances.get_all_accounts()
    if accounts:
        selected_account = st.selectbox("Sélectionnez un compte", accounts)
    else:
        selected_account = None
        st.warning("Aucun compte disponible. Créez-en un d'abord.")

    if selected_account:
        # Affichage du solde
        st.subheader(f"💳 Solde actuel de {selected_account}")
        balance = finances.get_balance(selected_account)
        st.info(f"💰 Solde : {balance} €")

        # Ajout d'argent
        st.header("➕ Ajouter de l'argent")
        add_amount = st.number_input("Montant à ajouter", min_value=0.0, step=1.0)
        if st.button("Ajouter"):
            finances.add_money(selected_account, add_amount)
            st.success(f"{add_amount} € ajouté au compte {selected_account}.")

        # Retrait d'argent
        st.header("➖ Retirer de l'argent")
        remove_amount = st.number_input("Montant à retirer", min_value=0.0, step=1.0)
        if st.button("Retirer"):
            if remove_amount > balance:
                st.error("Fonds insuffisants!")
            else:
                finances.remove_money(selected_account, remove_amount)
                st.success(f"{remove_amount} € retiré du compte {selected_account}.")

        # Transfert d'argent
        st.header("🔄 Transférer de l'argent")
        target_account = st.selectbox("Choisir un compte destinataire", [acc for acc in accounts if acc != selected_account])
        transfer_amount = st.number_input("Montant à transférer", min_value=0.0, step=1.0)
        if st.button("Transférer"):
            if transfer_amount > balance:
                st.error("Fonds insuffisants pour ce transfert!")
            else:
                finances.transfer_money(selected_account, target_account, transfer_amount)
                st.success(f"{transfer_amount} € transféré de {selected_account} vers {target_account}.")

        # Évolution du solde
        st.header("📈 Évolution du Solde")
        history = finances.get_history(selected_account)
        
        if history is not None and not history.empty:
            history["Cumulative Balance"] = history.apply(lambda row: row["Amount"] if row["Type"] == "Credit" else -row["Amount"], axis=1).cumsum()
            
            fig_balance = go.Figure()
            fig_balance.add_trace(go.Scatter(
                x=history.index,
                y=history["Cumulative Balance"],
                mode="lines+markers",
                name="Solde",
                line=dict(color="blue", width=2)
            ))
            fig_balance.update_layout(
                title=f"Évolution du Solde - {selected_account}",
                xaxis_title="Transactions",
                yaxis_title="Solde (€)",
                template="plotly_white"
            )
            st.plotly_chart(fig_balance)
        else:
            st.warning("Aucune transaction pour afficher l'évolution du solde.")

        # Tableau des transactions
        st.header("📋 Historique des Transactions")
        if history is not None and not history.empty:
            history["Date"] = pd.to_datetime(history.index).strftime("%Y-%m-%d %H:%M:%S")
            history_display = history[["Type", "Amount", "Date"]].rename(columns={"Type": "Nom", "Amount": "Montant (€)"})
            st.table(history_display)
        else:
            st.warning("Aucune transaction enregistrée.")

        # Suppression de compte
        st.header("🗑️ Supprimer un compte")
        if st.button("Supprimer ce compte"):
            finances.delete_account(selected_account)
            st.warning(f"Le compte '{selected_account}' a été supprimé.")
            st.experimental_rerun()

# ----------------------------- LOGIQUE PRINCIPALE -----------------------------
if not st.session_state.logged_in:
    login_page()
else:
    account_page()
