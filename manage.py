from flask import Flask
from flask_restful import Resource,Api

from service.proxy_service import FecthProxy

app = Flask(__name__)
api = Api(app)

api.add_resource(FecthProxy,'/')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=11110)
