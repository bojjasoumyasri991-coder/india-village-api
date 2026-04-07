from flask import Flask, jsonify, request
import pandas as pd
from flasgger import Swagger

swagger = Swagger(app)

app = Flask(__name__)

# Load dataset
df = pd.read_csv("india_villages.csv")

# ------------------ STATES API ------------------

@app.route('/states')
def get_states():

    states = df['State_name'].dropna().unique().tolist()

    return jsonify({
        "success": True,
        "count": len(states),
        "data": states
    })


# ------------------ DISTRICTS API ------------------

@app.route('/districts')
def get_districts():

    state = request.args.get('state')

    districts = df[df['State_name'] == state]['district_name'].dropna().unique().tolist()

    return jsonify({
        "success": True,
        "count": len(districts),
        "data": districts
    })


# ------------------ SUBDISTRICTS API ------------------

@app.route('/subdistricts')
def get_subdistricts():

    district = request.args.get('district')

    subdistricts = df[df['district_name'] == district]['subdistrict_name'].dropna().unique().tolist()

    return jsonify({
        "success": True,
        "count": len(subdistricts),
        "data": subdistricts
    })


# ------------------ VILLAGES API ------------------

@app.route('/villages')
def get_villages():

    subdistrict = request.args.get('subdistrict')
    limit = int(request.args.get('limit', 20))

    villages = df[df['subdistrict_name'] == subdistrict]['village_name'].dropna().tolist()

    villages = villages[:limit]

    return jsonify({
        "success": True,
        "count": len(villages),
        "data": villages
    })


# ------------------ SEARCH API ------------------

@app.route('/search')
def search_village():

    village = request.args.get('village')

    result = df[df['village_name'].str.contains(village, case=False, na=False)]

    result = result.head(20)

    data = []

    for _, row in result.iterrows():

        data.append({
            "village": row['village_name'],
            "subdistrict": row['subdistrict_name'],
            "district": row['district_name'],
            "state": row['State_name']
        })

    return jsonify({
        "success": True,
        "count": len(data),
        "data": data
    })


# ------------------ API DOCS ------------------

@app.route('/docs')
def api_docs():

    docs = {
        "API Documentation": {

            "1. Get States":
            "/states",

            "2. Get Districts":
            "/districts?state=HIMACHAL%20PRADESH",

            "3. Get Subdistricts":
            "/subdistricts?district=Kangra",

            "4. Get Villages":
            "/villages?subdistrict=Pangi",

            "5. Get Villages with Limit":
            "/villages?subdistrict=Pangi&limit=10",

            "6. Search Village":
            "/search?village=pan"
        }
    }

    return jsonify(docs)


if __name__ == "__main__":
    app.run(debug=True)
