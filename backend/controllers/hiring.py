import json
from flask import Blueprint, request, jsonify
from services.behavior_service import Behavior_Service
behavior_bp = Blueprint("behavior", __name__)

@behavior_bp.route("/track", methods=["POST"])
def track_code():
    return Behavior_Service.track_behavior()
