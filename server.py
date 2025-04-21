from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/coords", methods=["POST"])
def receive_coords():
    coords = request.get_json()
    with open("coordonnees_points.json", "w") as f:
        json.dump(coords, f)
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)
