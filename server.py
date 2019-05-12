# coding: utf-8
import time

from elasticsearch import Elasticsearch, RequestError
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
es = Elasticsearch(hosts=[({"host": "localhost", "port": 9200})])

INDEX_DOCUMENTS = "documents"
PROPERTY_TITLE = "title"
PROPERTY_CONTENT = "content"

# Configure index with our indexing preferences
print("Create and/or update index settings ...")
settings = {
    "analysis": {
        "analyzer": {
            "folding": {
                "tokenizer": "standard",
                "filter": ["lowercase", "asciifolding"]
            },
        }
    }
}

mapping = {
    "properties": {
        PROPERTY_TITLE: {
            "type": "text",
            "analyzer": "folding",
        },
        PROPERTY_CONTENT: {
            "type": "text",
            "analyzer": "folding",
        }
    }
}

try:
    es.indices.create(index=INDEX_DOCUMENTS)
except RequestError as exc:
    if exc.error == "resource_already_exists_exception":
        pass

es.indices.close(index=INDEX_DOCUMENTS)
es.indices.put_settings(index=INDEX_DOCUMENTS, body=settings)
es.indices.put_mapping(index=INDEX_DOCUMENTS, body=mapping)
es.indices.open(index=INDEX_DOCUMENTS)
print("ES index is ready")


@app.route("/", methods=["POST", "PUT"])
def post():
    id_ = request.json.get("id", int(round(time.time() * 1000)))
    res = es.index(index=INDEX_DOCUMENTS, id=id_, body={
        "title": request.json['title'],
        "content": request.json['content'],
    })
    return jsonify(res)


@app.route("/", methods=["PATCH"])
def patch():
    id_ = request.json["id"]
    body = {}

    if PROPERTY_TITLE in request.json:
        body[PROPERTY_TITLE] = request.json[PROPERTY_TITLE]

    if PROPERTY_CONTENT in request.json:
        body[PROPERTY_CONTENT] = request.json[PROPERTY_CONTENT]

    res = es.update(index=INDEX_DOCUMENTS, id=id_, body={"doc": body})
    return jsonify(res)


@app.route("/")
def get():
    search = request.args.get("search", "")
    # Add wildcard at end of each word (only at end for performances)
    search_string = ' '.join(map(lambda w: w + '*', search.split(' ')))
    print("search for: {}".format(search_string))

    if search:
        query = {
            "query": {
                "query_string": {
                    "query": search_string,
                    "fields": [PROPERTY_TITLE, PROPERTY_CONTENT]
                }
            }
        }
    else:
        query = {"query": {"match_all": {}}}

    res = es.search(index=INDEX_DOCUMENTS, body=query)
    return jsonify(res)
