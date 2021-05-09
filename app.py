from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db_actions import PostgersqlDBManagement
import db_actions
import json
import ast
app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app)

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

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

@app.route('/filter')
def page_filter():
    return render_template("filter.html")


@app.route('/view')
def page_view():
    return 'Page view'


@app.route('/process')
def page_process():
    return 'Page process'


if __name__ == '__main__':
    app.run()
