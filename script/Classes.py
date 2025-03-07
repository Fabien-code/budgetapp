import json
import pandas as pd
import numpy as np
import plotly.express as px

from dataclasses import dataclass
from config import LOGGING_LEVEL, DEFAULT_BALANCE, HISTORY_COLUMNS

import logging

# Configuration du logger pour afficher dans la console
logging.basicConfig(level=LOGGING_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ajoutez un StreamHandler pour rediriger les logs vers la console
console_handler = logging.StreamHandler()
console_handler.setLevel(LOGGING_LEVEL)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(console_handler)


@dataclass
class Compte:
    id_compte: str
    name: str
    balance: float
    history: pd.DataFrame

class App_Account:
    def __init__(self, name):
        self.name = name
        self.comptes = {}
        self.history = pd.DataFrame(columns=HISTORY_COLUMNS)

    def get_graph(self, name):
        """Génère un graphique Plotly de l'historique des transactions d'un compte."""
        if name in self.comptes:
            history = self.comptes[name].history
            if history.empty:
                logger.warning(f"Aucune transaction pour le compte {name}")
                return json.dumps({"error": "Aucune transaction pour ce compte."})

            fig = px.bar(history, x=history.index, y="Amount", color="Type",
                         labels={"index": "Transaction", "Amount": "Montant (€)"},
                         title=f"Historique des transactions pour {name}")

            return json.dumps(fig, cls=px.utils.PlotlyJSONEncoder)
        
        logger.error(f"Compte introuvable: {name}")
        return json.dumps({"error": "Compte introuvable."})

    def add_money(self, name, amount):
        """Ajoute de l'argent à un compte."""
        if name in self.comptes:
            self.comptes[name].balance += amount
            new_transaction = pd.DataFrame([["Credit", amount]], columns=HISTORY_COLUMNS)
            self.comptes[name].history = pd.concat([self.comptes[name].history, new_transaction], ignore_index=True)
            logger.info(f"{amount} € ajouté au compte {name}")
        else:
            logger.error(f"Compte introuvable: {name}")

    def remove_money(self, name, amount):
        """Retire de l'argent d'un compte."""
        if name in self.comptes:
            if self.comptes[name].balance >= amount:
                self.comptes[name].balance -= amount
                new_transaction = pd.DataFrame([["Debit", amount]], columns=HISTORY_COLUMNS)
                self.comptes[name].history = pd.concat([self.comptes[name].history, new_transaction], ignore_index=True)
                logger.info(f"{amount} € retiré du compte {name}")
            else:
                logger.warning(f"Fonds insuffisants pour retirer {amount} € du compte {name}")
        else:
            logger.error(f"Compte introuvable: {name}")

    def transfer_money(self, source, destination, amount):
        """Transfère de l'argent d'un compte à un autre."""
        if source in self.comptes and destination in self.comptes:
            if self.comptes[source].balance >= amount:
                self.remove_money(source, amount)
                self.add_money(destination, amount)
                logger.info(f"Transfert de {amount} € de {source} vers {destination}")
            else:
                logger.warning(f"Fonds insuffisants pour transférer {amount} € de {source} vers {destination}")
        else:
            logger.error(f"Compte source ({source}) ou destination ({destination}) introuvable.")

    def get_balance(self, name):
        """Retourne le solde d'un compte."""
        if name in self.comptes:
            return self.comptes[name].balance
        logger.error(f"Compte introuvable: {name}")
        return None

    def get_history(self, name):
        """Retourne l'historique des transactions d'un compte."""
        if name in self.comptes:
            return self.comptes[name].history
        logger.error(f"Compte introuvable: {name}")
        return None

    def create_account(self, name):
        """Crée un compte avec un solde initial défini dans config.py."""
        if name not in self.comptes:
            self.comptes[name] = Compte(id_compte=str(np.random.randint(10000, 99999)), name=name, balance=DEFAULT_BALANCE, history=pd.DataFrame(columns=HISTORY_COLUMNS))
            logger.info(f"Compte '{name}' créé avec succès.")
        else:
            logger.warning(f"Le compte '{name}' existe déjà.")

    def delete_account(self, name):
        """Supprime un compte existant."""
        if name in self.comptes:
            del self.comptes[name]
            logger.info(f"Compte '{name}' supprimé avec succès.")
        else:
            logger.error(f"Compte introuvable: {name}")

    def get_account(self, name):
        """Retourne un compte spécifique."""
        return self.comptes.get(name, None)

    def get_all_accounts(self):
        """Retourne tous les comptes existants."""
        logger.info(f"Comptes: {self.name}")
        return list(self.comptes)
def main():
    finances = App_Account(name="Finances")
    finances.create_account("Compte courant")
    finances.create_account("PEA")
    
    finances.add_money("Compte courant", 500)
    finances.transfer_money("Compte courant", "PEA", 200)
    
    logger.info(f"Solde Compte courant: {finances.get_balance('Compte courant')}")
    logger.info(f"Solde PEA: {finances.get_balance('PEA')}")
    logger.info(f"Historique Compte courant: {finances.get_history('Compte courant')}")

if __name__ == "__main__":
    main()
