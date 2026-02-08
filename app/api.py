from flask import Blueprint, request, jsonify
from app.db import list_reklamacje, list_reklamacje_by_status,add_reklamacja

api = Blueprint("api", __name__, url_prefix="/api")


def serialize_claim(row):
    """
    Convert DB row (tuple) to JSON-serializable dict.
    """
    return {
        "id": row[0],
        "data_zgloszenia": row[1],
        "tytul_zgloszenia": row[2],
        "ilosc": row[3],
        "status": row[4],
        "zglaszajacy": row[5],
        "claim_number": row[6],
    }


@api.get("/claims")
def get_claims():
    """
    GET /api/claims
    Optional query param: ?status=NOWE
    """
    status = request.args.get("status")

    if status:
        rows = list_reklamacje_by_status(status)
    else:
        rows = list_reklamacje()

    data = [serialize_claim(r) for r in rows]
    return jsonify(data)

@api.post("/claims")
def create_claim():
    """
    POST /api/claims
    Body: JSON
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Brak danych JSON"}), 400

    required_fields = [
        "data_zgloszenia",
        "tytul_zgloszenia",
        "ilosc",
        "zglaszajacy",
        "claim_number",
    ]

    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({
            "error": "Brak wymaganych pól",
            "missing_fields": missing
        }), 400

    try:
        add_reklamacja(
            data_zgloszenia=data["data_zgloszenia"],
            tytul_zgloszenia=data["tytul_zgloszenia"],
            opis=data.get("opis"),
            ilosc=int(data["ilosc"]),
            status="NOWE",
            zglaszajacy=data["zglaszajacy"],
            kod_wyrobu=data.get("kod_wyrobu"),
            nazwa_wyrobu=data.get("nazwa_wyrobu"),
            kkw=data.get("kkw"),
            claim_number=data["claim_number"],
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Zgłoszenie utworzone"}), 201
