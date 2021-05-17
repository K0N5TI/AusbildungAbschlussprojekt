from flask import Blueprint, jsonify, request
from db_actions import PostgersqlDBManagement
import json

config_interface = Blueprint(
    'config_interface', __name__, url_prefix="/config_interface")


@config_interface.route("/", methods=["GET"])
def get_config():
    with open("parameters.json") as file:
        data = json.load(file)
    json_data = {
        "postgres_url": data["postgres_url"],
        "postgres_user": data["postgres_user"],
        "postgres_db": data["postgres_db"],
        "limit_table_length": data["limit_table_length"],
        "export_path": data["export_path"]
    }
    return jsonify(json_data)


@config_interface.route("/", methods=["POST"])
def post_config():
    with open("parameters.json", 'r') as file:
        data = json.load(file)
    req = request.form
    accepted_parameters = ["postgres_url",
                           "postgres_user",
                           "postgres_pw",
                           "postgres_db",
                           "limit_table_length",
                           "export_path"]
    for parameter in accepted_parameters:
        if parameter in req:
            if req[parameter] != "":
                data[parameter] = req[parameter]

    with open("parameters.json", 'w') as file:
        json.dump(data, file, indent=4)
    return jsonify(success=True)


@config_interface.route("/reset", methods=["POST"])
def reset_config():
    with open("parameters.json", 'r') as file:
        data = json.load(file)
    standard_values = {}
    for key, value in data.items():
        if key.startswith("standard"):
            standard_values[key.replace("standard_", '')] = value
    for key in standard_values.keys():
        data[key] = standard_values[key]
    with open("parameters.json", 'w') as file:
        json.dump(data, file, indent=4)
    return jsonify(success=True)
