from flask import jsonify
from werkzeug.exceptions import HTTPException as _HTTPException


class RouterException(Exception):
  def __init__(self, message):
    super().__init__(message)


class HTTPException(_HTTPException):
  def __init__(self, code, description):
    self.code = code
    self.description = description
