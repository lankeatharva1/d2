"""
Customer Accounts Service

Paths:
------
GET    /accounts           - Returns a list of all Accounts
POST   /accounts           - Creates a new Account
GET    /accounts/{id}      - Returns the Account with a given id
PUT    /accounts/{id}      - Updates the Account with a given id
DELETE /accounts/{id}      - Deletes the Account with a given id
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_cors import CORS

# Create the Flask app
app = Flask(__name__)

# Security headers via Talisman (disable HTTPS redirect in testing)
talisman = Talisman(app, force_https=False)

# CORS policy
CORS(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///accounts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Import routes after app is created to avoid circular imports
from service import routes  # noqa: F401, E402
