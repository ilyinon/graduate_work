from typing import Callable, List

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.routing import APIRoute
from fastapi.security import HTTPBearer
from starlette.types import ASGIApp


class RBACMiddleware(type):
    def __new__(cls, name, bases, attrs, *kwargs):
        attrs["__init__"] = cls.add_role_check(attrs.get("__init__"))
        return super().__new__(cls, name, bases, attrs)

    @staticmethod
    def add_role_check(init_func: Callable):
        def wrapper(self, *args, *kwargs):
            init_func(self, *args, *kwargs)
            if hasattr(self, "route"):
                if hasattr(self.route, "roles"):
                    self.app.add_event_handler(
                        "startup", self.add_middleware_to_route(self.route)
                    )
        return wrapper

class RBACRoute(APIRoute):
    def __init__(self, *args, roles: List[str] = None, *kwargs):
        super().__init__(*args, *kwargs)
        self.roles = roles

class Authorize:
    def __init__(self, roles: List[str]):
        self.roles = roles

    def __call__(self, func):
        setattr(func, "roles", self.roles)
        return func

class RBACMiddleware(metaclass=RBACMiddleware):
    def __init__(self, app: ASGIApp, roles: List[str] = None):
        self.app = app
        self.roles = roles or []

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            route = request.scope.get("route")
            if route and hasattr(route, "roles"):
                if not any(role in self.roles for role in route.roles):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={
                            "message": "Not enough permissions",
                            "anonymous": not self.roles, # True если пользователь анонимный
                        }
                    )
        await self.app(scope, receive, send)

    def add_middleware_to_route(self, route: RBACRoute):
        async def middleware(request: Request, call_next):
            if not any(role in self.roles for role in route.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "message": "Not enough permissions",
                        "anonymous": not self.roles,
                    }
                )
            response = await call_next(request)
            return response
        route.endpoint = middleware