import json


def assert_index_handler_response(res):
  expected_index_handler_response = {"message": "hello"}
  assert json.loads(res.get_data(as_text=True)) == expected_index_handler_response


def assert_value_json_handler(res, value):
  expected_value_json_handler_response = {"value": value}
  assert json.loads(res.get_data(as_text=True)) == expected_value_json_handler_response 


def assert_client_response_http_methods(client, endpoint, http_methods):
  for method in http_methods:
    client_method = getattr(client, method)
    res = client_method(endpoint)

    assert_index_handler_response(res) 
