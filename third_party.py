from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/webhook/notifications/", methods=["POST"])
def webhook_notifications():
    """sample route used with e2e script to test the whole workflow"""

    payload = request.get_json()

    expected_fields = {"target_user_uuid", "url", "alert_uuid", "location", "label"}
    if not payload or not expected_fields.issubset(payload):
        return jsonify({"error": "Invalid payload"}), 400

    return jsonify({"status": "OK"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
