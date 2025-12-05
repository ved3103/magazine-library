# backend.py
from typing import Tuple

from flask import Flask, jsonify, request

from models import VALID_CATEGORIES
from storage import MagazineStorage

app = Flask(__name__)
storage = MagazineStorage()


def validate_magazine_payload(payload: dict) -> Tuple[bool, str]:
    """
    Validate JSON payload for creating a magazine.
    Returns (ok, error_message).
    """
    required = ["title", "publication_date", "editor", "category"]
    for field in required:
        if field not in payload or not str(payload[field]).strip():
            return False, f"Missing or empty field: {field}"

    if payload["category"] not in VALID_CATEGORIES:
        return False, (
            f"Invalid category '{payload['category']}'. "
            f"Allowed: {', '.join(VALID_CATEGORIES)}"
        )

    return True, ""


# -------- API endpoints --------
# (using /magazines..., but for your report you
# can say these are the media endpoints)

@app.route("/magazines", methods=["GET"])
def list_magazines():
    mags = storage.get_all()
    return jsonify([m.to_dict() for m in mags])


@app.route("/magazines/category/<category>", methods=["GET"])
def list_magazines_by_category(category: str):
    mags = storage.get_by_category(category)
    return jsonify([m.to_dict() for m in mags])


@app.route("/magazines/search", methods=["GET"])
def search_magazines():
    title = request.args.get("title", "")
    if not title:
        return jsonify({"error": "Query parameter 'title' is required"}), 400
    mags = storage.find_by_title_exact(title)
    return jsonify([m.to_dict() for m in mags])


@app.route("/magazines/<int:mag_id>", methods=["GET"])
def get_magazine(mag_id: int):
    mag = storage.get_by_id(mag_id)
    if mag is None:
        return jsonify({"error": "Magazine not found"}), 404
    return jsonify(mag.to_dict())


@app.route("/magazines", methods=["POST"])
def create_magazine():
    if not request.is_json:
        return jsonify({"error": "Body must be JSON"}), 400

    payload = request.get_json()
    ok, msg = validate_magazine_payload(payload)
    if not ok:
        return jsonify({"error": msg}), 400

    mag = storage.add_magazine(
        title=payload["title"],
        publication_date=payload["publication_date"],
        editor=payload["editor"],
        category=payload["category"],
    )
    return jsonify(mag.to_dict()), 201


@app.route("/magazines/<int:mag_id>", methods=["DELETE"])
def delete_magazine(mag_id: int):
    try:
        storage.delete_magazine(mag_id)
    except KeyError:
        return jsonify({"error": "Magazine not found"}), 404
    return "", 204


if __name__ == "__main__":
    # dev server
    app.run(debug=True)
