from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/products")
def products():
    return jsonify({"msg": "Products endpoint"})
