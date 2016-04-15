from flask import Flask, request, jsonify, render_template
from ntp.app import api

app = Flask(__name__)
app.debug = True


@app.route('/api/data', methods=["GET", "POST"])
def data():
    return api.get_demographic_data(request)


@app.route('/api/departments', methods=["GET"])
def departments():
    response = sorted(api.get_department_names("name"))
    return jsonify({"departments": response})


@app.route("/")
def index():
    return render_template("index.html")
