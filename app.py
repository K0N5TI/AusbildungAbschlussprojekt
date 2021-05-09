from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db_actions import PostgersqlDBManagement
from table import table_interface
import json
import ast

app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app)

app.register_blueprint(table_interface)

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
    table_names = database.get_table_names()
    for table in table_names:
        alltables.append({
            "table_name":str(table),
            "column_names":list(database.get_table_columns(table)),
            "table": database.get_table(table)
        })
    return render_template("db_view.html", alltables=alltables)

@app.route('/filter', methods=["GET", "POST"])
def page_filter():
    if request.method == "POST":
        req = request.form.to_dict()
        return redirect(url_for("page_view", parapeters=req), code=307)
    return render_template("filter.html")


@app.route('/view',methods=["GET", "POST"])
def page_view():
    if request.method == "GET":
        return redirect(url_for("alltables"))
    if request.method == "POST":
        #TODO Gefilterte Auswahl ausgeben statt alle Tabellen
        print(request.method)
        print(request.args)
    return redirect(url_for("alltables"))


@app.route('/process')
def page_process():
    return 'Page process'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
