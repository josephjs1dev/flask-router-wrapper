import time

from flask import jsonify, request
from flask_router_wrapper import Middleware


users = {}


def log_timestamp_middleware(next_function, *args, **kwargs):
  print("Current time:", time.time())
  return next_function(*args, **kwargs)


def not_authorized():
  return jsonify({"error": "not_authorized"}), 401


class AdminMiddleware(Middleware):
  def _exec(self, next_function, *args, **kwargs):
    token = request.headers.get("token", "")
    if token == "":
      return not_authorized()

    return next_function(*args, **kwargs)


def index_handler():
  return 'Hello, World!'


def get_users():
  return jsonify({"users": users})


def get_user(username):
  user = users.get(username, None)
  if not user:
    return jsonify({"error": "not_found"}), 404

  return jsonify(user)


def add_user():
  user_json = request.get_json()
  user = users.get(user_json["username"], None)
  if user:
    return jsonify(user), 201

  users[user_json["username"]] = user_json

  return jsonify(user_json), 201


def delete_user(username):
  user = users.get(username, None)
  if user:
    del users[username]

  return "", 204


def update_user(username):
  user_json = request.get_json()
  user = users.get(username, None)
  if not user:
    return jsonify({"error": "not_found"}), 404

  users[username] = user_json

  return jsonify(user_json)

