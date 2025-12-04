import json
from flask import Blueprint, request, jsonify
from services.tokenizer_service import tokenizer_service
inference_bp = Blueprint("deepseek", __name__)

@inference_bp.route("/question", methods=["POST"])
def run_inference():
    return tokenizer_service.run_inference()

@inference_bp.route("/compare_test" , methods =["POST"])
def compareCodes() : 
    return tokenizer_service.check_code()
