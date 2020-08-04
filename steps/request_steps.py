import os
import requests

from getgauge.python import step, data_store


TARGET_URL = os.environ.get('BRIGHTLOOM_INTEGRATION_TARGET')


def do_request(url, *args, method=requests.get, **kwargs):
    headers = kwargs.get('headers', {})
    token = data_store.scenario.get('token')
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data_store.scenario['result'] = method(
        f"{TARGET_URL}{url}", *args, headers=headers, **kwargs
    )


def response_to_curl(response):
    req = response.request

    command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    method = req.method
    uri = req.url
    data = req.body
    headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
    headers = " -H ".join(headers)
    return command.format(method=method, headers=headers, data=data, uri=uri)


def curl(response):
    return (
        " \n\nCurl command to "
        f"reproduce the request:\n{response_to_curl(response)}"
    )


@step("Request <url>")
def request_url(url):
    data_store.scenario['result'] = requests.get(f'{TARGET_URL}{url}')


@step("Response code is <code>")
def check_response_code(code):
    result = data_store.scenario.get('result')
    status_code = result.status_code
    assert int(status_code) == int(
        code
    ), f"Actual response code is {status_code}. {curl(result)}"


@step("Response is empty object")
def response_is_empty_object():
    result = data_store.scenario.get('result')
    assert (
        result.content == "{}"
    ), f"Response is not an empty object {result.content} .{curl(result)}"
