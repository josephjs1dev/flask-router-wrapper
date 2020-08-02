from flask import Flask
from flask_router_wrapper import RouterWrapper, BlueprintRouter

from .handler import *


def main():
  app = Flask(__name__)
  wrapper = RouterWrapper(app)

  wrapper.use(log_timestamp_middleware)
  wrapper.get('/', index_handler)

  # User domain
  user_group = BlueprintRouter("user", "user", url_prefix="/user")
  user_group.get('', get_users)
  user_group.get('/<username>', get_user)
  user_group.post('', AdminMiddleware(), add_user)
  user_group.put('/<username>', AdminMiddleware(), update_user)
  user_group.delete('/<username>', AdminMiddleware(), delete_user)

  wrapper.group('', user_group)
  wrapper.execute()

  app.run(port=8000, debug=True)


main()
