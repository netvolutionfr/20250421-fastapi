# FastAPI Product API

API REST construite avec [FastAPI](https://fastapi.tiangolo.com/), [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html), [Pydantic v2](https://docs.pydantic.dev/), et JWT pour l’authentification.

## Fonctionnalités

- CRUD sur les produits
- Liaison facultative avec des catégories
- Authentification par JWT (connexion + inscription)
- Réponses Pydantic avec relations imbriquées
- Routes protégées pour les opérations sensibles

## Installation

1. Clone du projet :

```bash
git clone https://github.com/netvolutionfr/20250421-fastapi.git
cd 20250421-fastapi
```

2. Créer un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sous Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancer le serveur

```bash
uvicorn main:app --reload
```

Accèder à la documentation interactive :

- [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Authentification

- `POST /register` — Crée un utilisateur
- `POST /login` — Renvoie un JWT
- Utiliser le bouton **Authorize** dans `/docs` avec le token JWT.

