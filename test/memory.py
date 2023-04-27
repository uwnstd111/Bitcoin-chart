import os
import importlib
from typing import Any
from psutil import Process


def format_output(mem: float) -> str:
    return f"(Memory usage: {mem:.2f} MB)"


def get_memory_usage() -> float:
    process = Process(os.getpid())
    megaBytes: float = process.memory_info().rss / (2**20)
    return megaBytes


class LazyImport:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module: Any | None = None

    def __getattr__(self, attr: str) -> Any:
        if self._module is None:
            self._module = importlib.import_module(self.module_name)
        return getattr(self._module, attr)


class TestMemory:

    def testNumpy(self):
        numpy: Any = LazyImport('numpy')
        memory = get_memory_usage()
        assert isinstance(numpy, LazyImport)
        assert isinstance(memory, float)

    def testFormat(self):
        used_memory: str = format_output(get_memory_usage())

        assert isinstance(used_memory, str)
        assert used_memory[-3:-1] == 'MB'

    def testUrlib(self):
        url_lib: Any = LazyImport('urllib.request')
        url = "https://pl.investing.com/crypto/bitcoin/historical-data"
        mem1 = get_memory_usage()
        request = url_lib.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        mem2 = get_memory_usage()

        assert isinstance(url_lib, LazyImport)
        assert mem1 < mem2
