from flask import Flask
import pytest


@pytest.fixture
def app():
  yield Flask(__name__)
