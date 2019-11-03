from os import getcwd
from json import loads
from flask import Flask, request
from flask_json import FlaskJSON, as_json, json_response
from pathalchemy import PathAlchemy
from configparser import ConfigParser
from flasgger import Swagger, swag_from

app = Flask(__name__)
FlaskJSON(app)
Swagger(app, template={
  "swagger": "2.0",
  "info": {
    "title": "PathQL API",
    "description": "PathQL API for my data",
    "version": "0.9.1"
  },
  "securityDefinitions": {
    "basicAuth": {
      "type": "basic"
    }
  },
  "security": [{      
      "basicAuth": []
    }
  ]
})

app.config['JSON_ADD_STATUS'] = False
config = None
cwd = getcwd()

@app.route('/pathql', methods=['POST'])
@swag_from(cwd+'/pathql.yml')
@as_json
def pathql():
    try:    
        username = config.get("flask", "username")
        password = config.get("flask", "password")
        if request.authorization:
            username = request.authorization.username
            password = request.authorization.password
        database = config.get("flask", "database")
        driver = config.get("flask", "driver")
        address = config.get("flask", "address")
        port = config.get("flask", "port")
        db = PathAlchemy.create(username,password,database,driver,address,port)
        data = request.get_json(force=True)
        result = db.path_query(data['query'],data['params'])
    except Exception as e:
        result = json_response(500, type=type(e).__name__, message=str(e))
    return result

if __name__ == '__main__':
    config = ConfigParser()
    config.read("config.ini")
    app.run()