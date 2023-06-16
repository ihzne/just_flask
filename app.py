from flask import Flask, request, render_template
from functools import wraps
import uuid

app = Flask(__name__)

def fake_middleware(func):
    @wraps(func)
    def wrapper(*args, **kws):
        print(request.endpoint)
        print(request.headers)

        x_attr = processXAttr(request.headers)

        if request.endpoint == "endpoint2":
            x_attr = str(uuid.uuid4())

        if x_attr is not None:
            return func(*args, **kws)
        else:
            return "Make a purchase to view!"
    return wrapper

def processXAttr(headers):
    x_attr = None
    if ("X-Attribute" not in headers or headers["X-Attribute"] is None):
        x_attr = headers["X-Attribute"]

    return x_attr

sold = 0
uuid_list = []

def update_sold_total(num):
    sold = sold + num

def get_sold_total(uuid):
    if (check_uuid_exist(uuid)):
        return sold
    else:
        return -1

def cache_uuid(uuid):
    uuid_list.add(uuid)

def check_uuid_exist(uuid):
    return uuid in uuid_list

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/endpoint1', methods=['GET'])
@fake_middleware
def endpoint1():
    cookies_total = get_sold_total(request.headers['X-Attribute'])
    return cookies_total

@app.route('/endpoint2', methods=['POST'])
@fake_middleware
def endpoint2():
    data = request.get_json()
    cookies_num = data.get('num')

    update_sold_total(cookies_num)
    cache_uuid(request.headers['X-Attribute'])

    return request.headers['X-Attribute']

def main(request):
    return app(request)