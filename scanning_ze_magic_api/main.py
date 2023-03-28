from flask import Flask, request, jsonify
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

@app.get('/test')
def get_test():
    return "Success"