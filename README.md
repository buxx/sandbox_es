# Install

## On dev machine

Start elastic search throught docker with:

    docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "cluster.routing.allocation.disk.threshold_enabled=false" elasticsearch:7.0.0

* Create virtualenv (python3)
* pip install -r requirements.txt

Start python http server with:

    FLASK_APP=server.py flask run

# Use

Install httpie with

    pip install httpie

Post documents (id is optional):

    http :5000 id=42 title=doc content="my doc content is awesome"

Update entire document:

    http :5000 id=42 title=doc2 content="my doc2 content is awesome"

Update part of document:

    http PATCH :5000 id=42 title="new doc2 title"

Get all index documents:

    http :5000

Make a search (search in title and content with "match" strategy)

    http ":5000?search=doç"

# Docker image

Build with:

    sudo docker build . -t sandbox-es

Start container with:

    sudo docker run -p 5000:5000 sandbox-es

Then use as explain at "Use" chapter
