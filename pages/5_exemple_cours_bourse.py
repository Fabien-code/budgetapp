import streamlit as st
import yfinance as yf
import pandas as pd

# 📌 Liste des 50 indices les plus connus
indices_populaires = {
    "S&P 500 (SPY)": "SPY",
    "NASDAQ 100 (QQQ)": "QQQ",
    "Dow Jones (DIA)": "DIA",
    "Russell 2000 (IWM)": "IWM",
    "FTSE 100 (UKX)": "^FTSE",
    "CAC 40 (FCHI)": "^FCHI",
    "DAX 40 (GDAXI)": "^GDAXI",
    "Nikkei 225 (N225)": "^N225",
    "Hang Seng (HSI)": "^HSI",
    "Euro Stoxx 50 (STOXX50E)": "^STOXX50E",
    "MSCI World (URTH)": "URTH",
    "MSCI Emerging Markets (EEM)": "EEM",
    "S&P/TSX Composite (TSX)": "^GSPTSE",
    "S&P ASX 200 (XJO)": "^AXJO",
    "S&P BSE Sensex (BSESN)": "^BSESN",
    "Nifty 50 (NSEI)": "^NSEI",
    "S&P Latin America 40 (ILF)": "ILF",
    "S&P Africa 40 (AFK)": "AFK",
    "Vanguard Total Stock Market (VTI)": "VTI",
    "Vanguard FTSE Developed Markets (VEA)": "VEA",
    "Vanguard FTSE Emerging Markets (VWO)": "VWO",
    "iShares MSCI ACWI (ACWI)": "ACWI",
    "iShares MSCI EAFE (EFA)": "EFA",
    "iShares China Large-Cap (FXI)": "FXI",
    "iShares Brazil (EWZ)": "EWZ",
    "iShares Germany (EWG)": "EWG",
    "iShares Japan (EWJ)": "EWJ",
    "iShares India (INDA)": "INDA",
    "iShares South Korea (EWY)": "EWY",
    "iShares Mexico (EWW)": "EWW",
    "iShares Canada (EWC)": "EWC",
    "iShares UK (EWU)": "EWU",
    "iShares France (EWQ)": "EWQ",
    "iShares Italy (EWI)": "EWI",
    "iShares Spain (EWP)": "EWP",
    "iShares Australia (EWA)": "EWA",
    "iShares Hong Kong (EWH)": "EWH",
    "iShares Singapore (EWS)": "EWS",
    "iShares Taiwan (EWT)": "EWT",
    "iShares Turkey (TUR)": "TUR",
    "iShares Russia (ERUS)": "ERUS",
    "iShares Saudi Arabia (KSA)": "KSA",
    "SPDR Gold Shares (GLD)": "GLD",
    "United States Oil Fund (USO)": "USO",
    "iShares Silver Trust (SLV)": "SLV",
    "Bitcoin ETF (BITO)": "BITO",
    "Ethereum ETF (ETHO)": "ETHO",
}

# 🎨 Interface utilisateur
st.title("📈 Simulation d'évolution d'un compte d'investissement")

# Sélection de l'indice via un menu déroulant
indice_selectionne = st.selectbox("🌍 Sélectionnez un indice ou ETF", list(indices_populaires.keys()))
ticker = indices_populaires[indice_selectionne]

# Entrée du capital initial
capital_initial = st.number_input("💰 Capital initial (€)", min_value=100, value=10000, step=100)

# Sélection de la période d'analyse
periode = st.selectbox("📅 Sélectionnez la période", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)

# Bouton pour lancer la simulation
if st.button("Lancer la simulation 🚀"):
    try:
        # Récupération des données
        data = yf.Ticker(ticker).history(period=periode)["Close"]
        data = data.pct_change().dropna()  # Calcul des rendements journaliers

        # Calcul du prix initial et des parts achetées
        prix_initial = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
        quantite_achetee = capital_initial / prix_initial

        # Simulation de l'évolution du solde
        solde = [capital_initial]
        for rendement in data:
            nouvelle_valeur = solde[-1] * (1 + rendement)
            solde.append(nouvelle_valeur)

        # Création du DataFrame
        df_resultat = pd.DataFrame({"Date": data.index, "Solde": solde[1:]})
        df_resultat.set_index("Date", inplace=True)

        # Affichage des résultats
        st.subheader(f"📊 Évolution du solde pour {indice_selectionne}")
        st.line_chart(df_resultat)

        # Affichage des stats finales
        st.write(f"📌 **Solde final estimé :** {solde[-1]:,.2f} €")
        st.write(f"📉 **Variation totale :** {((solde[-1] / capital_initial) - 1) * 100:.2f} %")

    except Exception as e:
        st.error(f"⚠️ Erreur lors de la récupération des données : {e}")
