import collections
import os
import json
import urllib
from typing import Dict

from flask import Flask, Response


app = Flask(__name__)


def flatten(d, parent_key="", sep="."):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def pull(url: str):
    resp = urllib.request.urlopen(url).read()
    data = json.loads(resp)
    print(data)
    return data


def format(data: Dict) -> str:
    lines = []
    for key, val in flatten(data).items():
        lines.append(f"{key} {val}")
    return "\n".join(lines)


@app.route("/")
def root():
    return """<!doctype html><html><a href="/metrics">Metrics</a></html>"""


@app.route("/metrics")
def metrics():
    url = os.getenv("URL")
    if url:
        return Response(format(pull(url)), mimetype="text/plain")
    else:
        return "URL environment variable (eg, http://x.x.x.x/air-data/latest) not set"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
