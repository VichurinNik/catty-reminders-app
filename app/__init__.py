import os
import json

with open('config.json') as config_json:
    config = json.load(config_json)
    users = config['users']
    db_path = config['db_path']

DEPLOY_REF = os.getenv("DEPLOY_REF", "NA")
