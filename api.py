import inspect

import parse
import webob


class API:

    def __init__(self):
        self.routes = {}

    def __call__(self, environ, start_response):
        request = webob.Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path):
        assert path not in self.routes, 'Such route already exists.'

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def default_response(self, response):
        response.status_code = 404
        response.text = 'Not found'

    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            parse_result = parse.parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        response = webob.Response()

        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError('Method not allowed', request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response
