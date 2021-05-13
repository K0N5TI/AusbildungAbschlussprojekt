from flask import Blueprint, jsonify, request, send_file, url_for, after_this_request
import pandas as pd
from db_actions import PostgersqlDBManagement
import json
from random import choice
from string import ascii_uppercase
import os
from io import BytesIO

export_interface = Blueprint(
    'export_interface', __name__, url_prefix="/export_interface")


def get_db_instance():
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                          url=data["postgres_url"], dbname=data["postgres_db"])
    return database


def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


@export_interface.route("/folder/csv")
def export_folder_csv():
    return ""


@export_interface.route("/folder/excel")
def export_folder_excel():
    return ""


@export_interface.route("/folder/pictures")
def export_folder_pictures():
    return ""


@export_interface.route("/download/csv")
def download_csv():
    return ""


@export_interface.route("/download/excel")
def download_excel():
    database = get_db_instance()
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    for table_name in database.get_table_names():
        data_list = [dict(row) for row in database.get_table(table_name, filter=request.values.to_dict())]
        if len(data_list) > 0:
            df = pd.DataFrame(data_list)
            df.columns = database.get_table_columns(table_name)
            df.to_excel(writer, sheet_name=str(table_name))
    writer.close()
    output.seek(0)
    return send_file(output, attachment_filename="testing.xlsx", as_attachment=True)


@export_interface.route("/download/pictures")
def download_pictures():
    return ""
