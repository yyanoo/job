###python flask 後端測試 db 用判斷是否output 有資料 需要在 wsl 環境進行測試 如flask後端 本身是需要使用 linux來進行部署測試

import importlib
import inspect
import pkgutil

from main import app
import api.lib as lib_pkg


def iter_noarg_functions(package):
    for module_info in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_info.name)

        for name, func in inspect.getmembers(module, inspect.isfunction):
            if func.__module__ != module.__name__:
                continue

            sig = inspect.signature(func)
            required_params = [
                p for p in sig.parameters.values()
                if p.default is inspect._empty
                and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
            ]

            if not required_params:
                yield module.__name__, name, func


if __name__ == "__main__":
    with app.app_context():
        for module_name, func_name, func in iter_noarg_functions(lib_pkg):
            try:
                result = func()
                ok = result is not None
                print(f"{module_name}.{func_name} -> {ok}")
            except Exception as e:
                print(f"{module_name}.{func_name} -> ERROR: {e}")