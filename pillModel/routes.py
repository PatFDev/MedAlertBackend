from flask import Blueprint, request, jsonify
from pillModel.utils import Model
from base64 import b64decode
from io import BytesIO
from PIL import Image

blueprint = Blueprint('model', __name__)

model = Model()

@blueprint.route("/apply", methods=["POST"])
def predict():
    '''
        Endpoint for handling prediction requests
    '''
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Check if 'image' key is in the request
        if "image" not in data:
            return jsonify({"error": "No image provided in the request."}), 400

        # Get the Base64 encoded image string
        base64_image = data["image"]

        # Make a prediction (predict method will handle Base64 decoding)
        prediction = model.predict(base64_image)

        return jsonify(prediction)
    except Exception as e:
        return jsonify({"error": f"Error during prediction: {str(e)}"}), 500


@blueprint.route("/test", methods=["GET"])
def test():
    # test endpoint to see if routes are working. ping method
    return jsonify({"message": "Model routes are working."}), 200
