from flask import Flask
from flask_router_wrapper import RouterWrapper, Router

from .handler import *


def main():
  app = Flask(__name__)
  wrapper = RouterWrapper(app)

  wrapper.use(log_timestamp_middleware)
  wrapper.get('/', index_handler)

  # User domain
  user_group = Router()
  user_group.get('', get_users)
  user_group.get('/<username>', get_user)
  user_group.post('', AdminMiddleware, add_user)
  user_group.put('/<username>', AdminMiddleware, update_user)
  user_group.delete('/<username>', AdminMiddleware, delete_user)

  wrapper.group('/user', user_group)
  wrapper.execute()

  app.run(port=8000, debug=True)


main()
