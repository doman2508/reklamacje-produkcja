"""Simple Flask frontend for the reklamacje app."""


from __future__ import annotations
from app.api import api

from flask import Flask, redirect, render_template, request, url_for

from app.db import add_reklamacja, list_reklamacje

from flask import request
from app.db import list_reklamacje_by_status


app = Flask(__name__)
app.register_blueprint(api)



@app.get("/")
def list_view():
    """Show claims, optionally filtered by status."""
    status = request.args.get("status")
    print("STATUS Z URL:", status)

    if status:
        reklamacje = list_reklamacje_by_status(status)
    else:
        reklamacje = list_reklamacje()

    return render_template(
        "list.html",
        reklamacje=reklamacje,
        selected_status=status
    )



@app.route("/add", methods=["GET", "POST"])
def add_view():
    """Display a form to add a claim and handle submissions."""
    if request.method == "POST":
        # Required fields.
        data_zgloszenia = request.form["data_zgloszenia"].strip()
        tytul_zgloszenia = request.form["tytul_zgloszenia"].strip()
        ilosc = int(request.form["ilosc"])

        # Optional fields.
        opis = request.form.get("opis", "").strip() or None
        zglaszajacy = request.form.get("zglaszajacy", "").strip() or None
        kod_wyrobu = request.form.get("kod_wyrobu", "").strip() or None
        nazwa_wyrobu = request.form.get("nazwa_wyrobu", "").strip() or None
        kkw = request.form.get("kkw", "").strip() or None
        claim_number = request.form.get("claim_number", "").strip() or None

        # Store the claim using the existing database helper.
        add_reklamacja(
            data_zgloszenia=data_zgloszenia,
            tytul_zgloszenia=tytul_zgloszenia,
            opis=opis,
            ilosc=ilosc,
            zglaszajacy=zglaszajacy,
            kod_wyrobu=kod_wyrobu,
            nazwa_wyrobu=nazwa_wyrobu,
            kkw=kkw,
            claim_number=claim_number,
        )
        return redirect(url_for("list_view"))

    return render_template("add.html")


if __name__ == "__main__":
    # Run the app for local development.
    app.run(host="0.0.0.0", port=5000, debug=True)
