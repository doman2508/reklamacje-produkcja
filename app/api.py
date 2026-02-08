from flask import Blueprint, request, jsonify
from app.db import list_reklamacje, list_reklamacje_by_status

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
