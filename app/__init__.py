"""
This module builds shared parts for other modules.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import json
import os

from fastapi.templating import Jinja2Templates


# --------------------------------------------------------------------------------
# Read Configuration
# --------------------------------------------------------------------------------

import os
import json

with open('config.json') as config_json:
    config = json.load(config_json)
    users = config['users']
    db_config = config.get('db_config', {})
    secret_key = config.get('secret_key', "Cats are awesome!")

DEPLOY_REF = os.getenv("DEPLOY_REF", "NA")

# --------------------------------------------------------------------------------
# Establish the Secret Key
# --------------------------------------------------------------------------------

secret_key = config['secret_key']


# --------------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------------

templates = Jinja2Templates(directory="templates")
