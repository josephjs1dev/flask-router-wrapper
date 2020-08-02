from flask import Flask
from flask_router_wrapper import RouterWrapper, Router, BlueprintRouter, RouterException

from tests.handler import index_handler
from tests.utils import *


def create_router(endpoint, http_methods, *handlers) -> Router:
  router = Router()

  for method in http_methods:
    router_method = getattr(router, method)
    router_method(endpoint, *handlers)

  return router


def create_blueprint_router(name, import_name, endpoint, http_methods,
                            *handlers) -> BlueprintRouter:
  router = BlueprintRouter(name, import_name)

  for method in http_methods:
    router_method = getattr(router, method)
    router_method(endpoint, *handlers)

  return router


def test_group_router_success(app: Flask):
  http_methods = ["get", "post", "put", "patch", "delete"]
  router = create_router("", http_methods, index_handler)

  wrapper = RouterWrapper(app)
  wrapper.group("/router", router)
  wrapper.execute()

  client = app.test_client()
  assert_client_response_http_methods(client, "/router", http_methods)


def test_group_blueprint_router_success(app: Flask):
  http_methods = ["get", "post", "put", "patch", "delete"]
  router = create_blueprint_router("blueprint", "blueprint", "", http_methods, index_handler)

  wrapper = RouterWrapper(app)
  wrapper.group("/blueprint", router)
  wrapper.execute()

  client = app.test_client()
  assert_client_response_http_methods(client, "/blueprint", http_methods)


def test_group_blueprint_router_in_router_success(app: Flask):
  http_methods = ["get", "post", "put", "patch", "delete"]
  blueprint_router = create_blueprint_router("blueprint", "blueprint", "", http_methods,
                                             index_handler)
  router = Router()
  router.group("/blueprint", blueprint_router)

  wrapper = RouterWrapper(app)
  wrapper.group("/router", router)
  wrapper.execute()

  client = app.test_client()
  assert_client_response_http_methods(client, "/router/blueprint", http_methods)


def test_group_router_in_blueprint_sucess(app: Flask):
  http_methods = ["get", "post", "put", "patch", "delete"]
  router = create_router("", http_methods, index_handler)
  blueprint_router = BlueprintRouter("blueprint", "blueprint")
  blueprint_router.group("/router", router)

  wrapper = RouterWrapper(app)
  wrapper.group("/blueprint", blueprint_router)
  wrapper.execute()

  client = app.test_client()
  assert_client_response_http_methods(client, "/blueprint/router", http_methods)


def test_group_not_router_or_blueprint(app: Flask):
  wrapper = RouterWrapper(app)
  err = None

  try:
    wrapper.group('', 'not_a_router')
  except RouterException as e:
    err = e

  assert err != None
  assert str(err) == "Not a Router or BlueprintRouter"
