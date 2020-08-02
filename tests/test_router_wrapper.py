from flask import Flask
from flask_router_wrapper import RouterWrapper, Router, RouterException
import pytest

from tests.handler import *
from tests.utils import *


@pytest.mark.parametrize("http_method", ["get", "post", "put", "patch", "delete"])
def test_router_wrapper_success(app: Flask, http_method: str):
  wrapper = RouterWrapper(app)
  wrapper_method = getattr(wrapper, http_method)
  wrapper_method('/', index_handler)
  wrapper.execute()

  client = app.test_client()
  client_method = getattr(client, http_method)
  res = client_method('/')

  assert_index_handler_response(res)


def test_router_empty_handler(app: Flask):
  wrapper = RouterWrapper(app)
  err = None

  try:
    wrapper.get('/')
  except RouterException as e:
    err = e

  assert err != None
  assert str(err) == "No handler given"


def test_router_not_callable(app: Flask):
  wrapper = RouterWrapper(app)
  err = None

  import inspect

  print(callable('not_a_handler'))
  try:
    wrapper.get('/', 'not_a_handler')
  except RouterException as e:
    err = e

  assert err != None
  assert str(
      err
  ) == "Only function or instance which is callable or inherits Middleware can be given as parameter"


def test_router_wrapper_route_success(app: Flask):
  wrapper = RouterWrapper(app)
  wrapper.route('/', ["GET", "POST"], index_handler)
  wrapper.execute()

  client = app.test_client()
  get_res = client.get('/')
  post_res = client.post('/')

  assert_index_handler_response(get_res)
  assert_index_handler_response(post_res)

  put_res = client.put('/')
  assert put_res.status_code == 405


def test_router_wrapper_route_not_accepted(app: Flask):
  wrapper = RouterWrapper(app)
  err = None

  try:
    wrapper.route('/', ["OTHER_NOT_ACCEPTED_METHOD"], index_handler)
  except RouterException as e:
    err = e

  assert err != None
  assert str(err) == "Method not accepted"


def test_router_wrapper_route_empty_method(app: Flask):
  wrapper = RouterWrapper(app)
  err = None

  try:
    wrapper.route('/', [], index_handler)
  except RouterException as e:
    err = e

  assert err != None
  assert str(err) == "No method given"
