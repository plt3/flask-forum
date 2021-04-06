import os

from elasticsearch import Elasticsearch
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_FORUM_SECRET_KEY")
postgresPwd = os.environ.get("POSTGRES_PASSWORD")
postgresUser = os.environ.get("POSTGRES_USER")
# postgresqlStr = f"postgresql://{postgresUser}:{postgresPwd}@localhost:5432/postgres"
postgresqlStr = f"postgresql://{postgresUser}:{postgresPwd}@db:5432/postgres"
app.config["SQLALCHEMY_DATABASE_URI"] = postgresqlStr
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///other.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ELASTICSEARCH_URL"] = os.environ.get("FLASK_FORUM_ES_URL")

app.elasticsearch = None
# app.elasticsearch = (
#     Elasticsearch([app.config["ELASTICSEARCH_URL"]])
#     if app.config["ELASTICSEARCH_URL"]
#     else None
# )

app.esPostIndexName = "posts"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from webApp import models, routes

if __name__ == "__main__":
    app.run(debug=True)
