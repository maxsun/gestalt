import flask
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import re

from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__, static_folder="./webclient/dist/", template_folder='./webclient/dist')
CORS(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.route('/')
def index():
    return 'Hello World'


app.run(debug=True)