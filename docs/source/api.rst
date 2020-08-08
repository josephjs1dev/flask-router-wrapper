Flask Router Wrapper API
==============================

This package wraps a Flask app and enables developer to add or grouping flask routing without the need to 
use Flask Application decorator. This wrapper is quite similar with how we define routing in Express. 
It only wraps Flask Application and defines its own Router class.

Router Wrapper
~~~~~~~~~~~~~~
Use this to wrap Flask Application.

.. autoclass:: flask_router_wrapper.RouterWrapper
    :members: 

Examples using RouterWrapper can be seen below.

.. literalinclude:: ../../examples/app_router.py
    :language: python
    :lines: 7-23

Router
~~~~~~~~~~~
.. autoclass:: flask_router_wrapper.Router
    :members:

Examples using Router can be seen below.

.. literalinclude:: ../../examples/app_group_router.py
    :language: python
    :lines: 7-25

Blueprint Router
~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: flask_router_wrapper.BlueprintRouter
    :members:

Examples using BlueprintRouter can be seen below.

.. literalinclude:: ../../examples/app_blueprint_router.py
    :language: python
    :lines: 7-25
