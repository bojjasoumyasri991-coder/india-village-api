from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

# Load dataset safely
df = pd.read_csv(
    "india_villages.csv",
    low_memory=False,
    on_bad_lines="skip"
)


@app.route("/")
def home():
    return render_template("home.html")
@app.route("/app")
def app_page():
    return render_template("index.html")


@app.route("/states")
def get_states():

    states = df["STATE NAME"].dropna().unique().tolist()

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

    districts = df[df["STATE NAME"] == state]["DISTRICT NAME"].dropna().unique().tolist()

    return jsonify({
        "success": True,
        "count": len(districts),
        "data": districts
    })


@app.route("/subdistricts")
def get_subdistricts():

    district = request.args.get("district")

    if not district:
        return jsonify({"error": "district parameter required"}), 400

    subdistricts = df[df["DISTRICT NAME"] == district]["SUB-DISTRICT NAME"].dropna().unique().tolist()

    return jsonify({
        "success": True,
        "count": len(subdistricts),
        "data": subdistricts
    })


@app.route("/villages")
def get_villages():
    import re

    subdistrict = request.args.get("subdistrict")

    if not subdistrict:
        return jsonify({"error": "subdistrict parameter required"}), 400

    limit = int(request.args.get("limit", 20))

    # Filter data
    villages_series = df[df["SUB-DISTRICT NAME"] == subdistrict]["Area Name"].dropna()

    # Clean villages in one step (optimized)
    cleaned_villages = (
        villages_series
        .astype(str)
        .apply(lambda x: re.sub(r"\(.*?\)", "", x))  # remove (numbers)
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
        "count": len(cleaned_villages),
        "data": cleaned_villages
    })

@app.route("/search")
def search_village():

    village = request.args.get("village")

    if not village:
        return jsonify({"error": "village parameter required"}), 400

    result = df[df["Area Name"].str.contains(village, case=False, na=False)]

    result = result.head(20)

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
            "Subdistricts": "/subdistricts?district=Kangra",
            "Villages": "/villages?subdistrict=Pangi",
            "Search": "/search?village=ram"
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)