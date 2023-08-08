from typing import Callable, Iterable, Any
from typing_extensions import NamedTuple
from http import HTTPMethod
import re


AnyPath = type("AnyPath", (), {})
NonePath = type("NonePath", (), {})


class RouterSignature(NamedTuple):
    handler: Callable
    var_names: Iterable[str]


class RouterTarget(NamedTuple):
    handler: Callable
    vars: dict[str, Any]


class Router:
    path_tree = {}
    r_braces = re.compile(r"^\{(\w+)\}$")

    def add_path(self, pattern: str, handler: Callable):
        items = [i for i in pattern.split("/") if i != ""]
        var_names = []
        p = self.path_tree
        for i in items:
            if m := re.match(Router.r_braces, i):
                var_names.append(m[1])
                if not p.get(AnyPath):
                    p[AnyPath] = {}
                p = p[AnyPath]
            else:
                if not p.get(i):
                    p[i] = {}
                p = p[i]
        p[NonePath] = RouterSignature(handler=handler, var_names=var_names)

    def get_target(self, path: str) -> RouterTarget | None:
        items = [i for i in path.split("/") if i != ""]
        values = []
        p = self.path_tree
        for i in items:
            # сначала проверяем на соответствие по строке,
            # если такого соответствия нет, то по
            if p.get(i):
                p = p[i]
            elif p.get(AnyPath):
                p = p[AnyPath]
                values.append(i)
            else:
                return None
        if np := p.get(NonePath):
            return RouterTarget(
                handler=np.handler,
                vars=dict(zip(np.var_names, values))
            )
        else:
            return None

    def func_decorator(self, method: HTTPMethod, path_pattern: str):
        def wrapper(func: Callable) -> Callable:
            self.add_path(path_pattern, func)
            return func
        return wrapper



# router = Router()
# router.add_path("/hello/{my}", lambda: 1)
# router.add_path("/abc/{id}/def/{di}", lambda: 2)
# router.add_path("/abc/{id}/d", lambda: 3)
#
# print(router.get_handler("/hello/sdf"))
# print(router.get_handler("/abc/_1_/def/_2_/"))
