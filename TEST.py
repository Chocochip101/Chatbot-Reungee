# -*- conding: utf-8 -*-
import math

from flask import Flask, request, jsonify

import random

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def webhook(originalDetectIntentRequest=None):
    return "Hello world"

if __name__ == '__main__':
    print("Hello ChatBot")
    app.run(host='0.0.0.0', port=5000)
