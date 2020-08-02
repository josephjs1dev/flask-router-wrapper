from flask import Flask
from flask_router_wrapper import RouterWrapper, Router, BlueprintRouter, RouterException

from tests.handler import *
from tests.utils import *


def test_middleware_function_success(app: Flask):
  wrapper = RouterWrapper(app)
  wrapper.use(set_value_middleware)
  wrapper.get("/", increment_value_middleware, value_json_handler)
  wrapper.execute()

  client = app.test_client("/")
  res = client.get("/")

  assert_value_json_handler(res, 1)


def test_middleware_instance_success(app: Flask):
  wrapper = RouterWrapper(app)
  wrapper.use(SetValueMiddleware())
  wrapper.get("/", IncrementValueMiddleware(), value_json_handler)
  wrapper.execute()

  client = app.test_client("/")
  res = client.get("/")

  assert_value_json_handler(res, 1)


def test_callable_instance_success(app: Flask):
  wrapper = RouterWrapper(app)
  wrapper.use(SetValueCallable())
  wrapper.get("/", IncrementValueCallable(), value_json_handler)
  wrapper.execute()

  client = app.test_client("/")
  res = client.get("/")

  assert_value_json_handler(res, 1)


def test_not_callable_instance_middleware(app: Flask):
  wrapper = RouterWrapper(app)
  err = None
  
  try: 
    wrapper.use(NotCallableMiddleware())
  except RouterException as e:
    err = e

  assert err != None
  assert str(err) == "Only function or instance which is callable or inherits Middleware can be given as parameter"


def test_use_for_group_router(app: Flask):
  wrapper = RouterWrapper(app)
  wrapper.use(SetValueMiddleware(), IncrementValueMiddleware())
  router = Router()
  router.use(IncrementValueMiddleware())
  router.get("", value_json_handler)
  wrapper.group("/router", router, IncrementValueMiddleware())
  wrapper.execute()

  client = app.test_client("/router")
  res = client.get("/router")

  assert_value_json_handler(res, 3) 


def test_use_for_group_blueprint_router(app: Flask):
  wrapper = RouterWrapper(app)
  wrapper.use(SetValueMiddleware(), IncrementValueMiddleware())
  router = BlueprintRouter("blueprint", "blueprint")
  router.use(IncrementValueMiddleware())
  router.get("", value_json_handler)
  wrapper.group("/blueprint", router, IncrementValueMiddleware())
  wrapper.execute()

  client = app.test_client("/blueprint")
  res = client.get("/blueprint")

  assert_value_json_handler(res, 3) 
