
from pathlib import Path
from os import name

EXT = 'dll' if name == 'nt' else 'so'


class GoWrapHandler:
    """
    Has a single one responsibility: compiling the wrapped go package
    """
    def __init__(self, root: Path, overwrite: bool = False) -> None:
        self.root_folder = root
        self.wrappers_file = root / '__go2py_wrappers.go'
        self.compiled_so = root / '__go2py_wrappers.{EXT}'
        self.wrappers_written = self.wrappers_file.exists() and not overwrite
        self.status_complete = self.compiled_so.exists() and not overwrite

    def compile(self):
        # todo
        ...
