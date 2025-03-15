import streamlit as st
import pandas as pd
import utils.accounts as accounts

# Titre de l'application
st.title("Répartition des Investissements")

# Vérifier si l'utilisateur est connecté
if "user" not in st.session_state:
    st.warning("Veuillez vous connecter d'abord.")
    st.switch_page("pages/1_Login.py")  # Redirige vers la connexion

username = st.session_state.user  # Récupérer l'utilisateur connecté

# Initialisation de l'instance de gestion des comptes pour cet utilisateur
if "finances" not in st.session_state or st.session_state.finances.username != username:
    st.session_state.finances = accounts.App_Account(username)

finances = st.session_state.finances

monthly_savings = st.number_input("Entrez vos revenus mensuels (€)", min_value=0, value=1000)

# Entrée utilisateur pour les 3 catégories d'investissement
epargne = st.number_input("Pourcentage investi en épargne/investissement", min_value=0, max_value=100, value=40)
st.text("Soit : {:.2f} €".format(monthly_savings * (epargne / 100)))
besoins = st.number_input("Pourcentage dépensé dans les besoins du quotidien", min_value=0, max_value=100, value=30)
st.text("Soit : {:.2f} €".format(monthly_savings * (besoins / 100)))
loisirs = st.number_input("Pourcentage dépensé dans les loisirs", min_value=0, max_value=100, value=30)
st.text("Soit : {:.2f} €".format(monthly_savings * (loisirs / 100)))

finances.split_savings = (epargne, besoins, loisirs)
# Vérification que le total est bien égal à 100%
total = epargne + besoins + loisirs

if total != 100:
    st.error("La somme des pourcentages doit être égale à 100% !")
else:
    # Création du graphique Camembert
    data_pie = pd.DataFrame({
        "Catégorie": ["Epargne", "Besoins", "Loisirs"],
        "Pourcentage": [epargne, besoins, loisirs]
    })
    st.subheader("Répartition des Investissements")
    st.pyplot(data_pie.plot.pie(y="Pourcentage", labels=data_pie["Catégorie"], autopct='%1.1f%%', legend=False).get_figure())

    duree = st.number_input("Durée de la projection en mois", min_value=0)+1
    st.title(f"Projection sur {duree-1} mois")

    # Calcul des projections
    capital = sum(finances.get_balance(account) for account in finances.get_all_accounts())
    projections = pd.DataFrame({
        "Mois": range(duree),
        "Epargne": [capital + monthly_savings * (epargne / 100) * i for i in range(duree)],
        "Besoins": [capital + monthly_savings * (besoins / 100) * i for i in range(duree)],
        "Loisirs": [capital + monthly_savings * (loisirs / 100) * i for i in range(duree)],
    })
    
    # Affichage du graphique avec des lignes
    st.subheader("Projection des investissements sur le temps")
    st.line_chart(projections.set_index("Mois"))
    st.text(f"Epargne dans {duree-1} mois: {projections['Epargne'].iloc[-1]:.2f} €")