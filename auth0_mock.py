import os
from collections import defaultdict

from flask import Flask, json, request
from jwcrypto import jwk, jwt

import collections
import logging

logger = logging.getLogger('auth0_mock')


def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source


def generate_mock_jwk_key_set():
    key = jwt.JWK(
        **{
            "k": os.environ.get('BRIGHTLOOM_INTEGRATION_MOCK_AUTH0_JWK_KEY'),
            "kid": "mock",
            "kty": "oct",
        }
    )
    jwk_set = jwk.JWKSet()
    jwk_set.add(key)
    return jwk_set.export()


api = Flask(__name__)

users = None
user_roles = None


@api.route('/cleanup', methods=['POST'])
def cleanup():
    global users, user_roles

    users = defaultdict(lambda: {'user_metadata': {}, 'app_metadata': {}})
    user_roles = defaultdict(lambda: set())

    return "ok"


@api.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    return generate_mock_jwk_key_set()


@api.route('/oauth/token', methods=['POST'])
def auth_token():
    return json.dumps({'access_token': '123'})


@api.route('/healthz', methods=['GET'])
def status():
    return json.dumps({'status': 'up'})


all_roles = {
    "Admin",
    "Brightloom Support Agent",
    "Member",
}


@api.route('/api/v2/users/<user_id>', methods=['GET', 'PATCH'])
def get_user(user_id):
    if request.method == 'PATCH':
        new_data = request.json
        users[user_id] = deep_update(users[user_id], new_data)
        logger.info(f"Updated user {user_id} with {new_data}")

    result = users[user_id]
    logger.info(f"Returned data for user {user_id}: {result}")
    return json.dumps(result)


@api.route('/api/v2/roles', methods=['GET'])
def get_roles():
    result = [{"id": x, "name": x} for x in all_roles]
    logger.info(f"Returned roles list: {result}")
    return json.dumps(result)


@api.route('/api/v2/users/<user_id>/roles', methods=['GET', 'POST', 'DELETE'])
def get_user_roles(user_id):
    ret_status = 200
    if request.method == 'DELETE':
        roles = set(request.json['roles'])
        user_roles[user_id] -= roles
        logger.info(f"Removed user {user_id} roles: {roles}")
        ret_status = 204

    if request.method == 'POST':
        roles = set(request.json['roles'])
        user_roles[user_id] |= roles
        logger.info(f"Added user {user_id} roles: {roles}")
        ret_status = 204

    result = [{"id": x, "name": x} for x in user_roles[user_id]]

    logger.info(f"Returned roles for user {user_id}: {result}")
    return json.dumps(result), ret_status


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    api.run(
        *os.environ.get(
            'BRIGHTLOOM_INTEGRATION_MOCK_AUTH0_LOCATION', 'localhost:8001'
        ).split(':')
    )
