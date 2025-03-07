from datetime import datetime
import streamlit as st
import pandas as pd
import utils.accounts as accounts
import plotly.graph_objects as go
# Initialisation de la session pour stocker les finances
if "finances" not in st.session_state:
    st.session_state.finances = accounts.App_Account()

finances = st.session_state.finances

st.title("💰 Gestion de Comptes Financiers")


st.title("📊 Vue Globale des Comptes")

# Récupération des comptes existants
accounts = finances.get_all_accounts()

if accounts:
    # Affichage des soldes sous forme de tableau
    st.header("💰 Soldes des Comptes")
    account_balances = {acc: finances.get_balance(acc) for acc in accounts}
    df_balances = pd.DataFrame(list(account_balances.items()), columns=["Compte", "Solde (€)"])
    st.table(df_balances)

    # Préparation des données pour le graphique d'évolution des soldes
    st.header("📈 Évolution des Soldes")
    fig = go.Figure()

    for acc in accounts:
        history = finances.get_history(acc)
        if history is not None and not history.empty:
            history["Cumulative Balance"] = history.apply(
                lambda row: row["Amount"] if row["Type"] == "Credit" else -row["Amount"], axis=1
            ).cumsum()

            fig.add_trace(go.Scatter(
                x=history.index,
                y=history["Cumulative Balance"],
                mode="lines+markers",
                name=acc
            ))

    fig.update_layout(
        title="Évolution des Soldes des Comptes",
        xaxis_title="Transactions",
        yaxis_title="Solde (€)",
        template="plotly_white"
    )

    st.plotly_chart(fig)

else:
    st.warning("Aucun compte disponible. Créez un compte d'abord.")


# Création de compte
st.header("🔹 Création de compte")
account_name = st.text_input("Nom du compte")
if st.button("Créer un compte"):
    if account_name:
        finances.create_account(account_name)
        st.success(f"Compte '{account_name}' créé avec succès!")
        st.rerun()

# Affichage des comptes existants
st.header("📜 Comptes existants")
accounts_list = finances.get_all_accounts()
if accounts_list:
    selected_account = st.selectbox("Sélectionnez un compte", accounts_list)

    # Affichage du solde
    balance = finances.get_balance(selected_account)
    st.info(f"💰 Solde actuel : {balance} €")

    # Ajouter de l'argent
    st.header("➕ Ajouter de l'argent")
    add_amount = st.number_input("Montant à ajouter", min_value=0.0, step=1.0)
    if st.button("Ajouter"):
        finances.add_money(selected_account, add_amount)
        st.success(f"{add_amount} € ajouté.")
        st.rerun()

    # Retirer de l'argent
    st.header("➖ Retirer de l'argent")
    remove_amount = st.number_input("Montant à retirer", min_value=0.0, step=1.0)
    if st.button("Retirer"):
        if remove_amount > balance:
            st.error("Fonds insuffisants!")
        else:
            finances.remove_money(selected_account, remove_amount)
            st.success(f"{remove_amount} € retiré.")
            st.rerun()

    # Transférer de l'argent
    st.header("🔄 Transférer de l'argent")
    target_account = st.selectbox("Choisir un compte destinataire", [acc for acc in accounts_list if acc != selected_account])
    transfer_amount = st.number_input("Montant à transférer", min_value=0.0, step=1.0)
    if st.button("Transférer"):
        if transfer_amount > balance:
            st.error("Fonds insuffisants!")
        else:
            finances.transfer_money(selected_account, target_account, transfer_amount)
            st.success(f"{transfer_amount} € transféré.")
            st.rerun()

    # Graphique d'évolution du solde
    st.header("📈 Évolution du Solde")
    fig_balance = finances.get_balance_graph(selected_account)
    if fig_balance:
        st.plotly_chart(fig_balance)
    else:
        st.warning("Aucune transaction enregistrée.")

    # Historique des transactions
    st.header("📋 Historique des Transactions")
    history = finances.get_history(selected_account)
    if history is not None and not history.empty:
        history["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.table(history[["Type", "Amount", "Date"]])
    else:
        st.warning("Aucune transaction.")

    # Suppression du compte
    if st.button("Supprimer ce compte"):
        finances.delete_account(selected_account)
        st.warning(f"Le compte '{selected_account}' a été supprimé.")
        st.rerun()
