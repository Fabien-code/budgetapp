import streamlit as st

def calculer_temps_objectif(revenus, depenses, montant_objectif):
    """Calcule le temps nécessaire pour atteindre l'objectif financier"""
    montant_epargne_mensuelle = max(revenus - depenses, 0)  # Évite une épargne négative
    if montant_epargne_mensuelle == 0:
        return float('inf')  # Si l'utilisateur ne peut pas épargner, objectif inatteignable
    mois_necessaires = montant_objectif / montant_epargne_mensuelle
    return mois_necessaires

def afficher_recommandations(revenus, depenses, objectif, montant_objectif):
    """Affiche une stratégie d'investissement pour atteindre l'objectif"""
    mois_necessaires = calculer_temps_objectif(revenus, depenses, montant_objectif)

    st.subheader(f"Stratégie pour atteindre votre objectif : {objectif}")
    
    st.write(f"Montant cible : **{montant_objectif} €**")
    st.write(f"Épargne mensuelle possible : **{revenus - depenses} €**")

    if mois_necessaires == float('inf'):
        st.error("⚠️ Vos dépenses sont trop élevées par rapport à vos revenus. Essayez de réduire vos dépenses ou d'augmenter vos revenus.")
    else:
        st.write(f"Temps estimé pour atteindre votre objectif : **{mois_necessaires:.1f} mois**")

    st.write("\n### Conseils :")
    if mois_necessaires > 60:  # Si plus de 5 ans pour atteindre l'objectif
        st.write("📌 Envisagez d'investir une partie de votre épargne dans des placements à rendement plus élevé pour accélérer l'atteinte de votre objectif.")
    if revenus - depenses < 200:
        st.write("📌 Vos marges d'épargne sont faibles. Essayez d'optimiser vos dépenses pour accélérer votre progression.")

def afficher_formulaire():
    """Affiche le formulaire de saisie pour l'utilisateur"""
    st.title("📊 Stratégie d'investissement personnalisée")

    revenus = st.number_input("💰 Entrez vos revenus mensuels (en €)", min_value=0, value=3000)
    depenses = st.number_input("📉 Entrez vos dépenses mensuelles (en €)", min_value=0, value=1500)
    
    objectif = st.text_input("🎯 Quel est votre objectif financier ? (ex: Achat appartement, Remboursement prêt, Voyage...)")
    montant_objectif = st.number_input("💵 Montant nécessaire pour cet objectif (en €)", min_value=0, value=20000)

    if st.button("🔍 Analyser ma capacité d'investissement"):
        if objectif and montant_objectif > 0:
            afficher_recommandations(revenus, depenses, objectif, montant_objectif)
        else:
            st.error("⚠️ Veuillez renseigner un objectif et un montant valide.")

# Exécution de l'application
afficher_formulaire()
