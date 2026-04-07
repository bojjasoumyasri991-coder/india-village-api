from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("india_villages.csv", low_memory=False)


@app.route('/states')
def get_states():

    states = df['STATE NAME'].dropna().unique().tolist()

    return jsonify({
        "success": True,
        "count": len(states),
        "data": states
    })


@app.route('/districts')
def get_districts():

    state = request.args.get('state')

    districts = df[df['STATE NAME'] == state]['DISTRICT NAME'].dropna().unique().tolist()

    return jsonify({
        "success": True,
        "count": len(districts),
        "data": districts
    })


@app.route('/subdistricts')
def get_subdistricts():

    district = request.args.get('district')

    subdistricts = df[df['DISTRICT NAME'] == district]['SUB-DISTRICT NAME'].dropna().unique().tolist()

    return jsonify({
        "success": True,
        "count": len(subdistricts),
        "data": subdistricts
    })


@app.route('/villages')
def get_villages():

    subdistrict = request.args.get('subdistrict')
    limit = int(request.args.get('limit', 20))

    villages = df[df['SUB-DISTRICT NAME'] == subdistrict]['Area Name'].dropna().tolist()

    villages = villages[:limit]

    return jsonify({
        "success": True,
        "count": len(villages),
        "data": villages
    })


@app.route('/search')
def search_village():

    village = request.args.get('village')

    result = df[df['Area Name'].str.contains(village, case=False, na=False)]

    result = result.head(20)

    data = []

    for _, row in result.iterrows():
        data.append({
            "village": row['Area Name'],
            "subdistrict": row['SUB-DISTRICT NAME'],
            "district": row['DISTRICT NAME'],
            "state": row['STATE NAME']
        })

    return jsonify({
        "success": True,
        "count": len(data),
        "data": data
    })


@app.route('/docs')
def api_docs():

    docs = {
        "API Documentation": {
            "1. Get States": "/states",
            "2. Get Districts": "/districts?state=HIMACHAL%20PRADESH",
            "3. Get Subdistricts": "/subdistricts?district=Kangra",
            "4. Get Villages": "/villages?subdistrict=Pangi",
            "5. Get Villages with Limit": "/villages?subdistrict=Pangi&limit=10",
            "6. Search Village": "/search?village=ram"
        }
    }

    return jsonify(docs)


if __name__ == "__main__":
    app.run(debug=True)