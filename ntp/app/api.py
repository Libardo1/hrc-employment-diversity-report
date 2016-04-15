from data.init_db import rdb_static, r
from flask import jsonify


def get_by_department(department, key_index):
    """
    Grab all data for each department from table.
    """

    output = [
       elem for elem in
        rdb_static
        .get_all(
            department,
            index=key_index
        ).run(r.connect())
    ]

    return output[0]


def get_department_names(department_key):
    """
    Return all department names for user selection.
    """

    output = [
        elem for elem in
        rdb_static
        .map(
            lambda row: row[department_key]
        )
        .distinct()
        .run(r.connect())
    ]

    return output


def get_demographic_data(request):
    if request.method == "POST":
        request_params = request.json.keys()

        if "attribute" not in request_params or "name" not in request_params:

            return jsonify(
                {"error": "Required key not found", "keys_found": request.json.keys()})

        attribute = request.json["attribute"]
        output = get_by_department(
            request.json["name"],
           "name" 
        )
        response = output[attribute]
        return jsonify({"attribute": response})

    if request.method == "GET":
        return jsonify({"status": "good"})


