from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="india_villages"
)

@app.route('/states')
def get_states():
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT state_name FROM villages")
    result = cursor.fetchall()

    states = [row[0] for row in result]

    return jsonify({
        "success": True,
        "count": len(states),
        "data": states
    })
@app.route('/districts')
def get_districts():
    state = request.args.get('state')

    cursor = db.cursor()
    query = "SELECT DISTINCT district_name FROM villages WHERE state_name = %s"
    cursor.execute(query, (state,))
    result = cursor.fetchall()

    districts = [row[0] for row in result]

    return jsonify({
        "success": True,
        "count": len(districts),
        "data": districts
    })
@app.route('/subdistricts')
def get_subdistricts():
    district = request.args.get('district')

    cursor = db.cursor()
    query = "SELECT DISTINCT subdistrict_name FROM villages WHERE district_name = %s"
    cursor.execute(query, (district,))
    result = cursor.fetchall()

    subdistricts = [row[0] for row in result]

    return jsonify({
        "success": True,
        "count": len(subdistricts),
        "data": subdistricts
    })
@app.route('/villages')
def get_villages():

    subdistrict = request.args.get('subdistrict')
    limit = request.args.get('limit', 20)

    cursor = db.cursor()

    query = """
    SELECT village_name
    FROM villages
    WHERE subdistrict_name = %s
    LIMIT %s
    """

    cursor.execute(query,(subdistrict,int(limit)))

    result = cursor.fetchall()

    villages = [row[0] for row in result]

    return jsonify({
        "success": True,
        "count": len(villages),
        "data": villages
    })
@app.route('/search')
def search_village():

    village = request.args.get('village')

    cursor = db.cursor()

    query = """
    SELECT village_name, subdistrict_name, district_name, state_name
    FROM villages
    WHERE village_name LIKE %s
    LIMIT 20
    """

    cursor.execute(query, ('%' + village + '%',))

    result = cursor.fetchall()

    data = []

    for row in result:
        data.append({
            "village": row[0],
            "subdistrict": row[1],
            "district": row[2],
            "state": row[3]
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
            
            "1. Get States":
            "http://127.0.0.1:5000/states",

            "2. Get Districts":
            "http://127.0.0.1:5000/districts?state=HIMACHAL%20PRADESH",

            "3. Get Subdistricts":
            "http://127.0.0.1:5000/subdistricts?district=Kangra",

            "4. Get Villages":
            "http://127.0.0.1:5000/villages?subdistrict=Pangi",

            "5. Get Villages with Limit":
            "http://127.0.0.1:5000/villages?subdistrict=Pangi&limit=10",

            "6. Search Village":
            "http://127.0.0.1:5000/search?village=pan"
        }
    }

    return jsonify(docs)
if __name__ == "__main__":
    app.run(debug=True)