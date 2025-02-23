from flask import Blueprint, request, jsonify
from ConflictionWarnings.utils import get_adverse_events

blueprint = Blueprint('confliction_warnings', __name__)

@blueprint.route('/check', methods=['POST'])
def check_interaction():
    """
    Endpoint to check for interactions between one drug and a list of drugs.
    """
    data = request.get_json()
    drug1 = data.get("drug1")
    drugs_list = data.get("drugs_list")

    if not drug1 or not drugs_list:
        return jsonify({"error": "Both drug1 and a list of drugs are required"}), 400

    all_interactions = {}

    for drug in drugs_list:
        interactions = get_adverse_events(drug1, drug)
        if "error" not in interactions:
            all_interactions[drug] = interactions
        else:
            all_interactions[drug] = []

    return jsonify({"drug1": drug1, "interactions": all_interactions}), 200



