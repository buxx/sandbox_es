# coding: utf-8
import time

from elasticsearch import Elasticsearch
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
es = Elasticsearch(hosts=[({"host": "localhost", "port": 9200})])

INDEX_DOCUMENTS = "documents"
DOC_TYPE_HTML = "html"


@app.route("/", methods=["POST"])
def post():
    id_ = request.json.get("id", int(round(time.time() * 1000)))
    res = es.index(index=INDEX_DOCUMENTS, doc_type=DOC_TYPE_HTML, id=id_, body={
        "title": request.json['title'],
        "content": request.json['content'],
    })
    return jsonify(res)


@app.route("/")
def get():
    search = request.args.get("search")
    # Add wildcard at end of each word (only at end for performances)
    search_string = ' '.join(map(lambda w: w+'*', search.split(' ')))
    print("search for: {}".format(search_string))

    if search:
        query = {
           "query": {
              "query_string": {
                 "query": search_string,
                 "fields": ["title", "content"]
              }
           }
        }
    else:
        query = {"query": {"match_all": {}}}

    res = es.search(index=INDEX_DOCUMENTS, body=query)
    return jsonify(res)
