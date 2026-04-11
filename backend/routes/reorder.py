from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from backend.models.db import db
from backend.models.inventory import Inventory

reorder_bp = Blueprint("reorder_bp", __name__)

@reorder_bp.route("/", methods=["GET"])
@jwt_required()
def get_reorder():
    try:
        low_stock_items = Inventory.query.filter(
            Inventory.quantity <= Inventory.reorder_level
        ).all()

        result = [
            {
                "id": item.id,
                "name": item.name,
                "quantity": item.quantity,
                "reorder_level": item.reorder_level
            }
            for item in low_stock_items
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500