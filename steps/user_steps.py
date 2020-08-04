import json
import os
from uuid import uuid4

import requests
from getgauge.python import step, data_store
from jwcrypto import jwt


EXAMPLE_USER__ADMIN1_USERNAME = os.environ.get('EXAMPLE_USER__ADMIN1_USERNAME')
EXAMPLE_USER__ADMIN1_PASSWORD = os.environ.get('EXAMPLE_USER__ADMIN1_PASSWORD')
EXAMPLE_USER__MEMBER1_USERNAME = os.environ.get(
    'EXAMPLE_USER__MEMBER1_USERNAME'
)
EXAMPLE_USER__MEMBER1_PASSWORD = os.environ.get(
    'EXAMPLE_USER__MEMBER1_PASSWORD'
)



@step("User is anonymous")
def anon_user():
    data_store.scenario['token'] = None
