import inspect
from typing import Callable, List, Type, Union, Dict, Tuple

from flask import Flask, Blueprint

from .exception import RouterException
from .middleware import Middleware, _FunctionMiddleware


class _BaseRouter:
  def __init__(self):
    self._global_middleware: List[Union[Middleware, Callable]] = []
    self._routes: Dict[Tuple[str], List[Callable]] = {}
    self._options: Dict[Tuple[str], dict] = {}
    self._blueprint_routes: List[BlueprintRouter] = []

  def use(self, *middleware: List[Union[Middleware, Callable]]):
    middleware = list(middleware)
    self._check_callable_or_middleware(middleware)
    self._global_middleware += middleware

  def group(self, prefix: str, router: Union["Router", "BlueprintRouter"],
            *middleware: List[Union[Middleware, Callable]]):
    middleware = list(middleware)
    self._check_callable_or_middleware(middleware)

    if issubclass(type(router), BlueprintRouter):
      router.url_prefix = prefix + (router.url_prefix or "")
      router._add_middleware_from_group(self._global_middleware + middleware)
      self._blueprint_routes.append(router)
      return

    routes: dict = router._routes
    for key, value in routes.items():
      handlers = value
      endpoint, methods = key
      new_key = (prefix + endpoint, methods)
      self._routes[new_key] = self._global_middleware + middleware + handlers
      self._options[new_key] = router._options[key]

    blueprint_routes = router._blueprint_routes
    for blueprint_route in blueprint_routes:
      blueprint_route.url_prefix = prefix + \
          (blueprint_route.url_prefix or "")
      blueprint_route._add_middleware_from_group(self._global_middleware + middleware)
      self._blueprint_routes.append(blueprint_route)

  def get(self, endpoint: str, *handlers: List[Union[Callable, Middleware]], **options):
    self.route(endpoint, ["GET"], *handlers)

  def post(self, endpoint: str, *handlers: List[Union[Callable, Middleware]], **options):
    self.route(endpoint, ["POST"], *handlers)

  def put(self, endpoint: str, *handlers: List[Union[Callable, Middleware]], **options):
    self.route(endpoint, ["PUT"], *handlers)

  def patch(self, endpoint: str, *handlers: List[Union[Callable, Middleware]], **options):
    self.route(endpoint, ["PATCH"], *handlers)

  def delete(self, endpoint: str, *handlers: List[Union[Callable, Middleware]], **options):
    self.route(endpoint, ["DELETE"], *handlers)

  def option(self, endpoint: str, *handlers: List[Union[Callable, Middleware]], **options):
    self.route(endpoint, ["OPTION"], *handlers)

  def route(self, endpoint: str, methods: List[str], *handlers: List[Union[Callable, Middleware]],
            **options):
    accepted_methods = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTION"]

    if len(methods) == 0:
      raise RouterException("No method given")

    if not all(method.upper() in accepted_methods for method in methods):
      raise RouterException("Method not accepted")

    handlers = list(handlers)
    self._check_handlers(handlers)

    key = (endpoint, "_".join(methods).upper())
    self._routes[key] = self._global_middleware + handlers
    self._options[key] = options

  @classmethod
  def _check_callable_or_middleware(cls, callable_list: List[Union[Callable, Middleware]]):
    for c in callable_list:
      if (inspect.isclass(c) and issubclass(c, Middleware)) or isinstance(
          c, Middleware) or callable(c):
        pass
      else:
        raise RouterException(
            "Only function or class which is callable or inherits Middleware can be given as parameter"
        )

  @classmethod
  def _check_handlers(cls, handlers: List[Union[Callable, Middleware]]):
    if len(handlers) == 0:
      raise RouterException("No handler given")
    else:
      cls._check_callable_or_middleware(handlers)

  @classmethod
  def _wrap_handlers(cls, handlers: List[Union[Callable, Middleware]]):
    handlers = handlers[::-1]
    handler = handlers.pop(0)
    middleware = handlers[0:]

    for m in middleware:
      if inspect.isclass(m) and issubclass(m, Middleware):
        instance: Middleware = m()
        handler = instance.add_next(handler)
      elif isinstance(m, Middleware):
        handler = m.add_next(handler)
      elif callable(m):
        mid = _FunctionMiddleware(m)
        handler = mid.add_next(handler)
      else:
        raise RouterException(
            "Only class which is callable or inherits Middleware can be given as parameter")

    return handler


class BlueprintRouter(_BaseRouter):
  def __init__(self, name, import_name, url_prefix=None, **kwargs):
    super().__init__()
    self.name = name
    self.import_name = import_name
    self.url_prefix = url_prefix
    self.kwargs = kwargs

  def group(self, prefix: str, router: "Router", *middleware: List[Union[Callable, Middleware]]):
    if not issubclass(type(router), Router) or len(router._blueprint_routes) > 0:
      raise RouterException("Only Core.Router class can be added")

    super().group(prefix, router, *middleware)

  def build_blueprint(self):
    blueprint = Blueprint(self.name, self.import_name, **self.kwargs)
    for key, handlers in self._routes.items():
      endpoint, req_types = key
      name = endpoint + req_types
      methods = req_types.upper().split("_")

      last_handler = handlers[-1]
      handler = self._wrap_handlers(handlers)
      setattr(handler, "__name__", getattr(last_handler, "__name__", ""))
      blueprint.route(endpoint,
                      endpoint=name,
                      methods=methods,
                      strict_slashes=False,
                      **self._options[key])(handler)

    return blueprint

  def _add_middleware_from_group(self, middleware: List[Union[Callable, Middleware]]):
    self._check_callable_or_middleware(middleware)
    for key, handlers in self._routes.items():
      self._routes[key] = middleware + handlers


class Router(_BaseRouter):
  pass


class RouterWrapper(_BaseRouter):
  def __init__(self, app: Flask):
    super().__init__()
    self.app = app

  def execute(self):
    for key, handlers in self._routes.items():
      endpoint, req_types = key
      name = endpoint + req_types
      methods = req_types.upper().split("_")

      last_handler = handlers[-1]
      handler = self._wrap_handlers(handlers)
      setattr(handler, "__name__", getattr(last_handler, "__name__", ""))
      self.app.route(endpoint,
                     endpoint=name,
                     methods=methods,
                     strict_slashes=False,
                     **self._options[key])(handler)

    for blueprint_route in self._blueprint_routes:
      self.app.register_blueprint(blueprint_route.build_blueprint(),
                                  url_prefix=blueprint_route.url_prefix)

  def add_error_handler(self, class_type: Type[Exception], handler: Callable):
    self.app.register_error_handler(class_type, handler)
