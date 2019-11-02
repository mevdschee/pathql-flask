from flask import Flask, request
from flask_json import FlaskJSON, as_json
from pathalchemy import PathAlchemy
from configparser import ConfigParser

app = Flask(__name__)
FlaskJSON(app)

app.config['JSON_ADD_STATUS'] = False
db = None

@app.route('/query', methods=['POST'])
@as_json
def query():
    data = request.get_json(force=True)
    return db.path_query(data['query'],data['params'])

if __name__ == '__main__':
    config = ConfigParser()
    config.read("config.ini")
    username = config.get("flask", "username")
    password = config.get("flask", "password")
    database = config.get("flask", "database")
    driver = config.get("flask", "driver")
    address = config.get("flask", "address")
    port = config.get("flask", "port")
    db = PathAlchemy.create(username,password,database,driver,address,port)
    app.run()