"""
Account Service Routes
"""
from flask import jsonify, request, abort
from service import app, db
from service.models import Account


@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "OK"}), 200


@app.route("/accounts", methods=["POST"])
def create_account():
    """Create a new Account"""
    data = request.get_json()
    if not data:
        abort(400, description="No data provided")
    account = Account().deserialize(data)
    db.session.add(account)
    db.session.commit()
    return jsonify(account.serialize()), 201


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""
    accounts = Account.query.all()
    return jsonify([a.serialize() for a in accounts]), 200


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Read a single Account"""
    account = Account.query.get_or_404(account_id)
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an Account"""
    account = Account.query.get_or_404(account_id)
    data = request.get_json()
    if not data:
        abort(400, description="No data provided")
    account.deserialize(data)
    db.session.commit()
    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an Account"""
    account = Account.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    return "", 204
