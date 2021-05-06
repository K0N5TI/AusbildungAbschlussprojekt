from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db_actions import PostgersqlDBManagement
import db_actions
import json
import ast
app = Flask(__name__)

app.config.from_object(Config())
db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    table_name = "trigger"
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                          url=data["postgres_url"], dbname=data["postgres_db"])
    return render_template("table_view.html", table_name=table_name, column_names=database.get_table_columns(table_name), table=database.get_table(table_name))


@app.route('/alltables')
def alltables():
    with open("parameters.json") as file:
        data = json.load(file)
        database = PostgersqlDBManagement(username=data["postgres_user"], password=data["postgres_pw"],
                                          url=data["postgres_url"], dbname=data["postgres_db"])
    alltables = []
    for table in database.get_table_names():
        alltables.append({
            "table_name":table,
            "column_names":database.get_table_columns(table),
            "table":database.get_table(table)
        })
    return render_template("db_view.html", alltables=alltables)

@app.route('/select')
def page_select():
    return 'Page select'


@app.route('/view')
def page_view():
    return 'Page view'


@app.route('/process')
def page_process():
    return 'Page process'


if __name__ == '__main__':
    app.run()
