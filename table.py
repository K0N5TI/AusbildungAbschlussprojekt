from flask import Blueprint, jsonify, request
from db_actions import PostgersqlDBManagement
import json

table_interface = Blueprint(
    'table_interface', __name__, url_prefix="/table_interface")


def get_db_instance():
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                          url=data["postgres_url"], dbname=data["postgres_db"])
    return database

@table_interface.route("/", methods=["GET"])
def get_table_names():
    database = get_db_instance()
    table_names = [*database.get_table_names()]
    return jsonify(columns=table_names)


@table_interface.route("/columns/<table_name>", methods=["GET"])
def get_table_columns(table_name):
    database = get_db_instance()
    return jsonify({"columns": [*database.get_table_columns(table_name)]})

@table_interface.route("/column/<table_name>/<column_name>", methods=["GET"])
def get_column_content(table_name, column_name):
    database = get_db_instance()
    return jsonify(database.get_table_column_values(table_name, column_name))


@table_interface.route("/rows/<table_name>", methods=["GET"])
def get_table_rows(table_name):
    database = get_db_instance()
    return jsonify({"data": [dict(row) for row in database.get_table(table_name, filter=request.values.to_dict())]})

@table_interface.route("/table/<table_name>", methods=["GET"])
def get_table(table_name):
    return get_table_columns(table_name).get_json() | get_table_rows(table_name).get_json()