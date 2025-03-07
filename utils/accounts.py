import pandas as pd
import numpy as np
import logging
import json
import os
import plotly.graph_objects as go

# Configuration du logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Paramètres globaux
DEFAULT_BALANCE = 0.0
HISTORY_COLUMNS = ["Type", "Amount"]
DATA_FILE = "accounts.json"

class Compte:
    def __init__(self, id_compte, name, balance=DEFAULT_BALANCE, history=None):
        self.id_compte = id_compte
        self.name = name
        self.balance = balance
        self.history = pd.DataFrame(history, columns=HISTORY_COLUMNS) if history else pd.DataFrame(columns=HISTORY_COLUMNS)

    def to_dict(self):
        """Convertir l'objet Compte en dictionnaire pour JSON."""
        return {
            "id_compte": self.id_compte,
            "name": self.name,
            "balance": self.balance,
            "history": self.history.to_dict(orient="records"),  # Convertir le DataFrame en liste de dictionnaires
        }

class App_Account:
    def __init__(self):
        self.comptes = {}
        self.load_from_file()  # Charger les comptes au démarrage

    def save_to_file(self):
        """Sauvegarde les comptes dans un fichier JSON."""
        data = {name: compte.to_dict() for name, compte in self.comptes.items()}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        """Charge les comptes depuis un fichier JSON."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    data = json.load(f)
                    for name, compte_data in data.items():
                        self.comptes[name] = Compte(
                            id_compte=compte_data["id_compte"],
                            name=compte_data["name"],
                            balance=compte_data["balance"],
                            history=compte_data["history"],
                        )
                    logger.info("Données chargées depuis le fichier JSON.")
                except json.JSONDecodeError:
                    logger.warning("Fichier JSON corrompu, création d'une nouvelle base de données.")
        else:
            logger.info("Aucun fichier JSON trouvé, création d'une nouvelle base de données.")

    def create_account(self, name):
        """Crée un compte avec un solde initial."""
        if name not in self.comptes:
            self.comptes[name] = Compte(id_compte=str(np.random.randint(10000, 99999)), name=name, balance=DEFAULT_BALANCE)
            self.save_to_file()
            logger.info(f"Compte '{name}' créé avec succès.")
        else:
            logger.warning(f"Le compte '{name}' existe déjà.")

    def get_all_accounts(self):
        """Retourne la liste des comptes."""
        return list(self.comptes.keys())

    def get_balance(self, name):
        """Retourne le solde du compte."""
        return self.comptes[name].balance if name in self.comptes else None

    def add_money(self, name, amount):
        """Ajoute de l'argent à un compte."""
        if name in self.comptes:
            self.comptes[name].balance += amount
            self.comptes[name].history = pd.concat(
                [self.comptes[name].history, pd.DataFrame([["Credit", amount]], columns=HISTORY_COLUMNS)],
                ignore_index=True,
            )
            self.save_to_file()

    def remove_money(self, name, amount):
        """Retire de l'argent d'un compte."""
        if name in self.comptes and self.comptes[name].balance >= amount:
            self.comptes[name].balance -= amount
            self.comptes[name].history = pd.concat(
                [self.comptes[name].history, pd.DataFrame([["Debit", amount]], columns=HISTORY_COLUMNS)],
                ignore_index=True,
            )
            self.save_to_file()

    def transfer_money(self, source, destination, amount):
        """Transfère de l'argent d'un compte à un autre."""
        if source in self.comptes and destination in self.comptes and self.comptes[source].balance >= amount:
            self.remove_money(source, amount)
            self.add_money(destination, amount)

    def get_history(self, name):
        """Retourne l'historique des transactions du compte."""
        return self.comptes[name].history if name in self.comptes else None

    def delete_account(self, name):
        """Supprime un compte."""
        if name in self.comptes:
            del self.comptes[name]
            self.save_to_file()

    def get_balance_graph(self, name):
        """Génère un graphique d'évolution du solde."""
        if name in self.comptes:
            history = self.get_history(name)
            if history is not None and not history.empty:
                history["Cumulative Balance"] = history.apply(
                    lambda row: row["Amount"] if row["Type"] == "Credit" else -row["Amount"], axis=1
                ).cumsum()

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=history.index,
                    y=history["Cumulative Balance"],
                    mode="lines+markers",
                    name="Solde",
                    line=dict(color="blue", width=2),
                ))
                fig.update_layout(
                    title=f"Évolution du Solde - {name}",
                    xaxis_title="Transactions",
                    yaxis_title="Solde (€)",
                    template="plotly_white",
                )
                return fig
        return None
