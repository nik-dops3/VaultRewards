from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
import json

# ─────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────

app = Flask(__name__)
CORS(app)

# In production these come from AWS Secrets Manager
# For local development they come from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "vaultrewards")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# ─────────────────────────────────────────────
# In-memory data store for local development
# In production this is Aurora PostgreSQL
# ─────────────────────────────────────────────

members = {
    "M001": {
        "id": "M001",
        "name": "Sarah Johnson",
        "email": "sarah@example.com",
        "tier": "Gold",
        "points": 4250,
        "card_number": "4532 **** **** 1234",
        "joined": "2024-01-15",
        "monthly_fee": 9.99
    },
    "M002": {
        "id": "M002",
        "name": "James Williams",
        "email": "james@example.com",
        "tier": "Platinum",
        "points": 12800,
        "card_number": "4532 **** **** 5678",
        "joined": "2023-11-20",
        "monthly_fee": 29.99
    },
    "M003": {
        "id": "M003",
        "name": "Emma Davis",
        "email": "emma@example.com",
        "tier": "Silver",
        "points": 890,
        "card_number": "4532 **** **** 9012",
        "joined": "2024-03-01",
        "monthly_fee": 0
    }
}

# Points multiplier per tier
TIER_MULTIPLIERS = {
    "Silver": 1,
    "Gold": 2,
    "Platinum": 3
}

# ─────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────

@app.route("/health")
def health():
    # This endpoint is called by:
    # - The load balancer every 30 seconds to check if the API is alive
    # - The CI/CD pipeline after deployment to verify success
    # - Kubernetes liveness probe to know if the pod needs restarting
    return jsonify({
        "status": "healthy",
        "environment": ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }), 200

# ─────────────────────────────────────────────
# Member Endpoints
# ─────────────────────────────────────────────

@app.route("/members", methods=["GET"])
def get_all_members():
    # Returns all members — used by the admin dashboard
    return jsonify({
        "members": list(members.values()),
        "total": len(members)
    }), 200


@app.route("/members/<member_id>", methods=["GET"])
def get_member(member_id):
    # Returns one member's details — used by the member portal
    member = members.get(member_id)
    if not member:
        return jsonify({
            "error": "Member not found",
            "member_id": member_id
        }), 404
    return jsonify(member), 200


@app.route("/members", methods=["POST"])
def create_member():
    # Creates a new member — called when someone signs up
    data = request.get_json()

    # Validate required fields
    required = ["name", "email", "tier"]
    for field in required:
        if field not in data:
            return jsonify({
                "error": f"Missing required field: {field}"
            }), 400

    # Validate tier
    if data["tier"] not in TIER_MULTIPLIERS:
        return jsonify({
            "error": f"Invalid tier. Must be Silver, Gold, or Platinum"
        }), 400

    # Generate member ID
    member_id = f"M{str(len(members) + 1).zfill(3)}"

    # Set monthly fee based on tier
    fees = {"Silver": 0, "Gold": 9.99, "Platinum": 29.99}

    new_member = {
        "id": member_id,
        "name": data["name"],
        "email": data["email"],
        "tier": data["tier"],
        "points": 0,
        "card_number": f"4532 **** **** {member_id[1:]}",
        "joined": datetime.utcnow().strftime("%Y-%m-%d"),
        "monthly_fee": fees[data["tier"]]
    }

    members[member_id] = new_member

    return jsonify({
        "message": "Member created successfully",
        "member": new_member
    }), 201

# ─────────────────────────────────────────────
# Points Endpoints
# ─────────────────────────────────────────────

@app.route("/members/<member_id>/points", methods=["GET"])
def get_points(member_id):
    # Returns a member's points balance
    member = members.get(member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    return jsonify({
        "member_id": member_id,
        "name": member["name"],
        "tier": member["tier"],
        "points_balance": member["points"],
        "multiplier": TIER_MULTIPLIERS[member["tier"]]
    }), 200


@app.route("/members/<member_id>/points/add", methods=["POST"])
def add_points(member_id):
    # Adds points after a card transaction
    # In production this is triggered by Lambda via SQS
    # For local development we call it directly
    member = members.get(member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    data = request.get_json()
    if "amount_spent" not in data:
        return jsonify({"error": "Missing amount_spent"}), 400

    amount = float(data["amount_spent"])
    multiplier = TIER_MULTIPLIERS[member["tier"]]

    # Points formula: £1 spent = 1 base point x tier multiplier
    points_earned = int(amount * multiplier)
    member["points"] += points_earned

    return jsonify({
        "member_id": member_id,
        "amount_spent": amount,
        "multiplier": multiplier,
        "points_earned": points_earned,
        "new_balance": member["points"],
        "transaction_time": datetime.utcnow().isoformat()
    }), 200

# ─────────────────────────────────────────────
# Admin Endpoints
# ─────────────────────────────────────────────

@app.route("/admin/stats", methods=["GET"])
def get_stats():
    # Used by the admin dashboard
    total_points = sum(m["points"] for m in members.values())
    revenue = sum(m["monthly_fee"] for m in members.values())

    tier_breakdown = {}
    for tier in TIER_MULTIPLIERS:
        tier_members = [m for m in members.values() if m["tier"] == tier]
        tier_breakdown[tier] = len(tier_members)

    return jsonify({
        "total_members": len(members),
        "total_points_liability": total_points,
        "monthly_revenue": round(revenue, 2),
        "tier_breakdown": tier_breakdown,
        "environment": ENVIRONMENT
    }), 200

# ─────────────────────────────────────────────
# Run the app
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=ENVIRONMENT == "development"
    )
