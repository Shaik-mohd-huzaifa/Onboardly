from flask import request
import json

def NormalizeData(data):
    normalizing_data = data.decode("utf-8")
    return json.loads(normalizing_data)