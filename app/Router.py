import re

from loguru import logger

from singleton import SingletonMeta


class Router(metaclass=SingletonMeta):
    def __init__(self):
        self.routes = {
            'GET': {},
            'POST': {},
            'DELETE': {},
        }

    def add_route(self, method, path, handler):
        compiled = re.compile(path)
        self.routes[method][compiled] = handler

    def resolve(self, method, path) -> callable:
        logger.info(f'Resolving {method} {path}')
        if method not in self.routes:
            return None

        for pattern, handler in self.routes[method].items():
            if pattern.match(path):
                return handler
        return None
