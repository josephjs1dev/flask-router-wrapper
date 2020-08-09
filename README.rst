====================
Flask-Router-Wrapper
====================

|Build Status| |Coverage| |License|

A flask wrapper that wraps flask current decorator router. Flask-Router-Wrapper is inspired by router from Express.
Flask-Router-Wrapper enables adding middleware to application handler without using decorator and also grouping routers and handlers.

Installation
------------

Install the extension with using pip, or easy\_install.

.. code:: bash

    $ pip install flask-router-wrapper

Examples
--------

Examples can be seen in `here <https://github.com/josephsalimin/flask-router-wrapper/tree/master/examples>`__ 

Tests
-----

Tests can be run using pytest. 

.. code:: bash

    $ pytest --cov-report=xml --cov=flask_router_wrapper ./tests

Contributing
------------

Questions, comments, or improvements? Feel free to create issues or pull request on
`Github <https://github.com/josephsalimin/flask-router-wrapper>`__

.. |Build Status| image:: https://github.com/josephsalimin/flask-router-wrapper/workflows/Build/badge.svg
   :target: https://github.com/josephsalimin/flask-router-wrapper/actions
.. |Coverage| image:: https://codecov.io/gh/josephsalimin/flask-router-wrapper/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/josephsalimin/flask-router-wrapper
.. |License| image:: http://img.shields.io/:license-mit-blue.svg
