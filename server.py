from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route("/<string:name>", methods=["POST"])
def deploy(name):
    command = [os.path.expanduser("~/code/pi-deployer/run_script.sh"), name]
    subprocess.run(command)
    return jsonify("Successfully redeployed"), 200

if __name__ == "__main__":
    app.run(debug=True, port=8888)
