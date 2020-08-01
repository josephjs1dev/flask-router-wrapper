from flask import Flask
from flask_router_wrapper import RouterWrapper

from .handler import *


def main():
  app = Flask(__name__)
  wrapper = RouterWrapper(app)

  wrapper.use(log_timestamp_middleware)
  wrapper.get('/', index_handler)

  # User domain
  wrapper.get('/user', get_users)
  wrapper.get('/user/<username>', get_user)
  wrapper.post('/user', AdminMiddleware, add_user)
  wrapper.put('/user/<username>', AdminMiddleware, update_user)
  wrapper.delete('/user/<username>', AdminMiddleware, delete_user)

  wrapper.execute()

  app.run(port=8000, debug=True)


main()
