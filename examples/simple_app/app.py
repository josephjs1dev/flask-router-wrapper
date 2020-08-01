import random
import time

from flask import Flask, g
from flask_router_wrapper import RouterWrapper, Router, BlueprintRouter, Middleware

name_list = ['Luffy', 'Chopper', 'Yamato']


def log_timestamp_middleware(next_function, *args, **kwargs):
  print("Current time:", time.time())
  return next_function(*args, **kwargs)


class RandomNameMiddleware(Middleware):
  def _exec(self, next_function, *args, **kwargs):
    g.random_name = random.choice(name_list)

    return next_function(*args, **kwargs)


def random_name_middleware(next_function, *args, **kwargs):
  g.random_name = random.choice(name_list)

  return next_function(*args, **kwargs)


def index_handler():
  return 'Hello, World!'


def random_name_handler():
  return 'Your name is: ' + g.random_name


def user_group_log_middleware(next_function, *args, **kwargs):
  print("User data", args, kwargs)

  return next_function(*args, **kwargs)


def user_group_middleware(next_function, name):
  g.admin = name == 'admin'
  return next_function(name)


def user_info_handler(name):
  return "Hello, {}! Your admin status: {}".format(name, g.admin)


def main():
  app = Flask(__name__)
  wrapper = RouterWrapper(app)

  wrapper.use(log_timestamp_middleware)
  wrapper.get('/', index_handler)
  wrapper.get('/random_name_1', random_name_middleware, random_name_handler)
  wrapper.get('/random_name_2', RandomNameMiddleware, random_name_handler)
  wrapper.get('/random_name_3', RandomNameMiddleware(), random_name_handler)

  random_name_group = Router()
  random_name_group.post('', random_name_handler)

  user_group = BlueprintRouter("user", "user")
  user_group.use(user_group_log_middleware)
  user_group.group('/random', random_name_group, random_name_middleware)
  user_group.get('/<name>', user_group_middleware, user_info_handler)

  wrapper.group("/user", user_group)
  wrapper.execute()

  app.run(port=8000)


main()
