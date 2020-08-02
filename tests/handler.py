from flask import g, jsonify
from flask_router_wrapper import Middleware


class SetValueMiddleware(Middleware):
  def _exec(self, next_function, *args, **kwargs):
    g.val = 0
    return next_function(*args, **kwargs)


class IncrementValueMiddleware(Middleware):
  def _exec(self, next_function, *args, **kwargs):
    g.val += 1
    return next_function(*args, **kwargs)


class SetValueCallable:
  def __call__(self, next_function, *args, **kwargs):
    g.val = 0
    return next_function(*args, **kwargs)


class IncrementValueCallable:
  def __call__(self, next_function, *args, **kwargs):
    g.val += 1
    return next_function(*args, **kwargs)


class NotCallableMiddleware:
  pass


def set_value_middleware(next_function, *args, **kwargs):
  g.val = 0
  return next_function(*args, **kwargs)


def increment_value_middleware(next_function, *args, **kwargs):
  g.val += 1
  return next_function(*args, **kwargs)


def index_handler():
  return jsonify({"message": "hello"})


def value_json_handler():
  return jsonify({"value": g.val})
