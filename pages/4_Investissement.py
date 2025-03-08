import streamlit as st

# Fonction pour calculer les conseils en fonction du revenu et des objectifs
def donner_conseils(finances):
    revenus = finances["revenus"]
    objectifs = finances["objectifs"]

    # Règle 50/30/20
    besoins = revenus * 0.50
    envies = revenus * 0.30
    epargne = revenus * 0.20

    st.subheader("Voici vos conseils financiers basés sur la règle 50/30/20 :")
    
    st.write(f"**50% pour les besoins :** {besoins} €")
    st.write(f"**30% pour les envies :** {envies} €")
    st.write(f"**20% pour l'épargne et le remboursement des dettes :** {epargne} €")
    
    st.write("\n")

    # Conseils supplémentaires en fonction des objectifs
    if "épargne" in objectifs:
        st.write("Conseil : Vous devriez vous concentrer sur la construction d'une épargne d'urgence avant d'augmenter vos dépenses.")
    if "remboursement de dettes" in objectifs:
        st.write("Conseil : Priorisez le remboursement de vos dettes, surtout celles à taux d'intérêt élevé.")
    if "investissements" in objectifs:
        st.write("Conseil : Une fois vos dettes sous contrôle, pensez à investir une partie de votre épargne dans des placements à long terme.")
    
    st.write("\n")
    
    st.write("N'oubliez pas que ces conseils doivent être adaptés en fonction de votre situation personnelle.")

# Formulaire pour recueillir les informations financières de l'utilisateur
def afficher_formulaire():
    st.title("Conseils financiers personnalisés")

    revenus = st.number_input("Entrez vos revenus mensuels (en €)", min_value=0, value=2000)
    depenses = st.number_input("Entrez vos dépenses mensuelles (en €)", min_value=0, value=1000)

    objectifs = []
    if st.checkbox("Épargner pour l'avenir"):
        objectifs.append("épargne")
    if st.checkbox("Rembourser des dettes"):
        objectifs.append("remboursement de dettes")
    if st.checkbox("Investir pour la retraite"):
        objectifs.append("investissements")

    if st.button("Obtenir des conseils"):
        finances = {
            "revenus": revenus,
            "depenses": depenses,
            "objectifs": objectifs
        }
        donner_conseils(finances)

# Afficher le formulaire
afficher_formulaire()
