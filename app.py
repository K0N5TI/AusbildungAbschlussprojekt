from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db_actions import PostgersqlDBManagement
import table
import export
import json
import ast

app = Flask(__name__)
app.config.from_object(Config())
with open("parameters.json") as file:
    data = json.load(file)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{data["postgres_user"]}:{data["postgres_pw"]}@{data["postgres_url"]}/{data["postgres_db"]}'
db = SQLAlchemy(app)

app.register_blueprint(table.table_interface)
app.register_blueprint(export.export_interface)
app.jinja_env.globals.update(get_table_columns=table.get_table_columns)


@app.route('/')
def hello_world():

    return render_template("index.html",)


@app.route('/alltables')
def alltables():
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                          url=data["postgres_url"], dbname=data["postgres_db"])
    alltables = []
    table_names = database.get_view_names()
    table_names.extend(database.get_table_names())
    for i in table_names:
        alltables.append({
            "table_name": str(i)
        })
    return render_template("db_view.html", alltables=alltables)


@app.route('/filter', methods=["GET", "POST"])
def page_filter():
    if request.method == "POST":
        return redirect(url_for("page_view"), code=307)
    return render_template("filter.html")


@app.route('/view', methods=["GET"])
def page_view():
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                        url=data["postgres_url"], dbname=data["postgres_db"])
    req = request.values.to_dict()
    for key in [*req]:
        if req[key] == 'Choose...' or req[key] == '':
            del req[key]
        elif req[key] == 'on':
            req[key] = True
    alltables = []
    table_names = database.get_view_names()
    for table_name in table_names:
        alltables.append({
            "table_name": str(table_name),
            "parameters": req
        })
    return render_template("db_view.html", alltables=alltables)


@app.route('/process', methods=["GET", "POST"])
def page_process(parameters=None):
    parameters= request.values.to_dict()
    return render_template("processing.html")


@app.route('/view/<table_name>')
def view_table(table_name):
    return render_template("ajax_table_view.html", table_name=table_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
