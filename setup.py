from setuptools import setup
from os.path import join, dirname

with open(join(dirname(__file__), 'flask_router_wrapper/version.py'), 'r') as f:
  exec(f.read())

setup(name='Flask-Router-Wrapper',
      version=__version__,
      url='https://github.com/josephsalimin/flask-router-wrapper',
      license='MIT',
      description=
      'A Flask extension which wraps flask application router',
      long_description=open('README.rst').read(),
      packages=['flask_router_wrapper'],
      install_requires=["Flask>=1.1.2"],
      python_requires='>=3.6.*')
