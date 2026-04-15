from flask import Flask, jsonify, request, render_template
import pandas as pd
from functools import lru_cache
import re

app = Flask(__name__)


# ✅ Load only required columns + cache (VERY IMPORTANT)
@lru_cache(maxsize=1)
def load_data():
    return pd.read_csv(
        "india_villages.csv",
        usecols=["STATE NAME", "DISTRICT NAME", "SUB-DISTRICT NAME", "Area Name"],
        dtype=str,
        low_memory=True
    )


df = load_data()


# -------------------- ROUTES --------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/app")
def app_page():
    return render_template("index.html")


@app.route("/states")
def get_states():
    states = sorted(df["STATE NAME"].dropna().unique().tolist())

    return jsonify({
        "success": True,
        "count": len(states),
        "data": states
    })


@app.route("/districts")
def get_districts():
    state = request.args.get("state")

    if not state:
        return jsonify({"error": "state parameter required"}), 400

    districts = (
        df[df["STATE NAME"] == state]["DISTRICT NAME"]
        .dropna()
        .unique()
        .tolist()
    )

    return jsonify({
        "success": True,
        "count": len(districts),
        "data": sorted(districts)
    })


@app.route("/subdistricts")
def get_subdistricts():
    district = request.args.get("district")

    if not district:
        return jsonify({"error": "district parameter required"}), 400

    subdistricts = (
        df[df["DISTRICT NAME"] == district]["SUB-DISTRICT NAME"]
        .dropna()
        .unique()
        .tolist()
    )

    return jsonify({
        "success": True,
        "count": len(subdistricts),
        "data": sorted(subdistricts)
    })


@app.route("/villages")
def get_villages():
    subdistrict = request.args.get("subdistrict")

    if not subdistrict:
        return jsonify({"error": "subdistrict parameter required"}), 400

    limit = int(request.args.get("limit", 20))

    villages = df[df["SUB-DISTRICT NAME"] == subdistrict]["Area Name"].dropna()

    # ✅ Clean data
    cleaned = (
        villages.astype(str)
        .apply(lambda x: re.sub(r"\(.*?\)", "", x))
        .str.replace("R.F.", "", regex=False)
        .str.replace("D.P.F.", "", regex=False)
        .str.strip()
        .drop_duplicates()
        .sort_values()
        .head(limit)
        .tolist()
    )

    return jsonify({
        "success": True,
        "count": len(cleaned),
        "data": cleaned
    })


@app.route("/search")
def search_village():
    village = request.args.get("village")

    if not village:
        return jsonify({"error": "village parameter required"}), 400

    result = df[df["Area Name"].str.contains(village, case=False, na=False)].head(20)

    data = []

    for _, row in result.iterrows():
        data.append({
            "village": row["Area Name"],
            "subdistrict": row["SUB-DISTRICT NAME"],
            "district": row["DISTRICT NAME"],
            "state": row["STATE NAME"]
        })

    return jsonify({
        "success": True,
        "count": len(data),
        "data": data
    })


@app.route("/docs")
def docs():
    return jsonify({
        "API Endpoints": {
            "States": "/states",
            "Districts": "/districts?state=HIMACHAL%20PRADESH",
            "Subdistricts": "/subdistricts?district=Chamba",
            "Villages": "/villages?subdistrict=Pangi",
            "Search": "/search?village=ram"
        }
    })


# -------------------- RUN --------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
