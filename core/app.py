import json
import sys
import urllib

from include.codes import *

sys.path.append('../')


class Application:

    def __init__(self, routers, controllers):
        self.routers = routers
        self.controllers = controllers

    def __call__(self, env, start_response):
        uri = self.check_uri(env['PATH_INFO'])
        print(env)
        method = env['REQUEST_METHOD']

        query_params = self.parse_params(env['QUERY_STRING'])
        print(query_params)

        input_data = self.get_wsgi_input(env)
        # Если Пришел json, десериализуем с помощью json.loads, иначе - парсим функцией parse_params
        if 'CONTENT_TYPE' in env and env['CONTENT_TYPE'] == 'application/json':
            input_data = json.loads(input_data)
        else:
            input_data = self.parse_params(input_data)

        if uri in self.routers:
            view = self.routers[uri]
            request = {}
            for controller in self.controllers:
                controller(request)
            request['method'] = method
            request['query_params'] = query_params
            request['data'] = input_data
            code, response_body = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [response_body.encode('utf-8')]
        else:
            start_response(NOT_FOUND_404, [('Content-Type', 'text/html')])
            return [b"Page not found"]

    @staticmethod
    def check_uri(uri):
        if not uri.endswith('/'):
            uri += '/'
        return uri

    @staticmethod
    def parse_params(params):
        param_dict = {}
        if params:
            param_list = params.split('&')
            for param in param_list:
                k, v = param.split('=')
                k = urllib.parse.unquote_plus(k)
                v = urllib.parse.unquote_plus(v)
                param_dict.update({k: v})
        return param_dict

    @staticmethod
    def get_wsgi_input(env):
        content_len = env.get('CONTENT_LENGTH')
        content_len = int(content_len) if content_len else 0
        return env['wsgi.input'].read(content_len).decode('utf-8') if content_len > 0 else ''
