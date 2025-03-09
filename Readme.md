
# BudgetApp

**BudgetApp** est une application web permettant de gérer ses finances personnelles. L'application permet aux utilisateurs de se connecter, de consulter leurs dépenses et d'ajouter de nouvelles transactions. Elle est construite avec **Streamlit** pour l'interface utilisateur et **Firebase** pour la gestion des utilisateurs et des données en temps réel.

## Fonctionnalités

- Connexion et authentification des utilisateurs.
- Gestion des dépenses personnelles.
- Visualisation des dépenses sous forme de graphiques.
- Ajout et suppression de transactions.

## Prérequis

Avant de commencer, assurez-vous que vous avez les éléments suivants installés sur votre machine :

- **Python 3.x** : Télécharger et installer depuis [python.org](https://www.python.org/downloads/).
- **Streamlit** : Utilisé pour le développement de l'interface utilisateur.
- **Firebase** : Utilisé pour gérer les utilisateurs et stocker les données des transactions.

### Installation

Clonez le repository et installez les dépendances avec `pip` :

```bash
git clone https://github.com/ton-compte/budgetapp.git
cd budgetapp
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt
```

### TODO 

Ajouter les virements suggérés a faire par l'utilisateur pour respecter les splits
ajt un type epargen ou compte courant 
Faire renseigner à l'user les taux et la date d'augmentation des taux pour ces comptes
faire en sorte de pouvoir traquer les etf/actions pour le pea etc => exemple temporaire page 5
