from io import TextIOWrapper
from os import PathLike
from pathlib import Path
import re
from typing import Callable, Type

from go2py.symbols import GoFunc, GoStruct, Symbol
from go2py.wrapper_handler import GoWrapHandler


GO_FUNC_RE = re.compile(
    r'^func +?(?P<method_of>\([^()]+\))? *'
    r'(?P<name>[^()]*) ?'
    r'\((?P<args>[^()]*?)\) *'
    r'(?P<returned>.*?) *?{'
)

GO_STRUCT_RE = re.compile(
    r'^type (?P<name>.*?) struct *?{'
)

SYMBOLS_KNOWN: list[tuple[re.Pattern, Type[Symbol]]] = [(GO_FUNC_RE, GoFunc), (GO_STRUCT_RE, GoStruct)]


class Reader:
    """Reads the go package. Generates extensions"""
    _active_readers: list['Reader'] = []

    def __init__(self, file: PathLike, overwrite_wraphandler: bool=False, wrap_unexported: bool = False) -> None:
        self.root = Path(file)
        self.wrap_unexported = wrap_unexported
        self.update_package()
        self._active_readers.append(self)
        self.go_wrap_handler = GoWrapHandler(self.root, overwrite_wraphandler)

    def update_package(self):
        self.package: str = None
        self.symbols: dict[str, Symbol] = {}
        if self.root.is_file():
            self.root = self.root.parent
        for file in self.root.iterdir():
            if not file.is_file() and file.suffix == '.go':
                continue
            self._read_file(file)

    def seek_package(self, f: TextIOWrapper):
        while not (first_line := next(f)).startswith("package"):
            continue
        return first_line.removeprefix('package').split('//', 1)[0].strip()

    def _read_file(self, file: Path):
        with file.open('r', encoding='utf-8') as f:
            if self.package is None:
                self.package = self.seek_package(f)
            self._get_symbols(f)

    def _get_symbols(self, f: TextIOWrapper):
        contents = f.read()
        for pattern, symbol_type in SYMBOLS_KNOWN:
            for m in re.finditer(pattern, contents):
                symbol = symbol_type.from_match(m)
                if symbol.exported or self.wrap_unexported:
                    symbol.wrap(self.go_wrap_handler)
                    self.symbols[symbol.name] = symbol.name

    @classmethod
    def get(cls, file: PathLike, **kwargs) -> 'Reader':
        """Returns the valid Reader from the package or creates one if none exists"""
        file = Path(file)
        if file.is_file():
            def is_of_the_same_package(f: Path, root: Path):
                return f.parent.absolute() == root.absolute()
        elif file.is_dir():
            def is_of_the_same_package(f: Path, root: Path):
                return f.absolute() == root.absolute()
        else:
            raise ValueError(f"Unhandled filetype: {file!s}")

        for reader in cls._active_readers:
            if is_of_the_same_package(file, reader.root):
                return reader
        return cls(file, **kwargs)


    def wrap_function(
        self, function_name: str,
        accept_methods: bool = False, accept_generic: bool = False
    ) -> Callable:
        ...

    @classmethod
    def wrap_struct(
        self, struct_name: str,
        constructor: str = None, wrap_methods: bool = True
    ) -> type:
        ...