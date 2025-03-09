import streamlit as st
from openai import OpenAI
import utils.accounts as accounts

# Vérifier si l'utilisateur est connecté
if "user" not in st.session_state:
    st.warning("Veuillez vous connecter d'abord.")
    st.switch_page("pages/1_Login.py")  # Redirige vers la connexion

# Initialise le client DeepSeek
client = OpenAI(api_key=st.secrets["AI"]["token"], base_url="https://api.deepseek.com")

username = st.session_state.user  # Récupérer l'utilisateur connecté


# Initialisation de l'instance de gestion des comptes pour cet utilisateur
if "finances" not in st.session_state or st.session_state.finances.username != username:
    st.session_state.finances = accounts.App_Account(username)

finances = st.session_state.finances

capital = 0
accounts_list = finances.get_all_accounts()
for account in accounts_list:
    capital += finances.get_balance(account)

# Fonction pour générer une stratégie d'investissement personnalisée
def get_investment_advice(capital, savings, risk_tolerance, purpose, horizon, preferences):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an expert financial advisor specialized in investments."},
            {"role": "user", "content": 
                f"I want to invest my money but I'm not sure how to proceed. "
                f"Here is my financial situation:\n"
                f"- Initial capital: ${capital}\n"
                f"- Monthly savings: ${savings}\n"
                f"- Risk tolerance: {risk_tolerance}\n"
                f"My purpose: {purpose}\n"
                f"- Investment horizon: {horizon} years\n"
                f"- Preferences: {preferences}\n\n"
                "Can you provide an optimized investment strategy with a diversified portfolio? "
                "Please include percentage allocation and explanations for each choice."
                "At the end, provide a percentage split advicebetween my needs, savings and pleasures expenses"
            }
        ],
        stream=False
    )
    
    return response.choices[0].message.content

# Interface utilisateur Streamlit pour saisir les informations financières
st.title("Personalized Investment Strategy")

if finances.monthly_savings is None:
    monthly_savings = st.number_input("Enter your monthly savings ($)", min_value=0, value=1000)
if finances.risk_tolerance is None:
    risk_tolerance = st.selectbox("Select your risk tolerance", ["Low", "Moderate", "High"])
if finances.purpose is None:
    purpose = st.text_input("Enter your investment purpose (e.g., Buy a flat, Retirement, etc.)", "Buy a flat in 15 years")
if finances.horizon is None:
    horizon = st.number_input("Enter your investment horizon (in years)", min_value=1, value=15)
if finances.preferences is None:
    preferences = st.text_input("Enter your investment preferences (e.g., ETFs, real estate, cryptocurrency)", "ETFs, real estate, cryptocurrency")

# Bouton pour obtenir des conseils
if st.button("Get Investment Advice"):
    advice = get_investment_advice(capital, monthly_savings, risk_tolerance, purpose, horizon, preferences)
    st.subheader("Investment Strategy Advice:")
    st.write(advice)
