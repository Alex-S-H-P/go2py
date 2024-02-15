from abc import ABC, abstractmethod
import re
import sys
from go2py.wrapper_handler import GoWrapHandler

if sys.version_info > (3, 10):
    from typing import Self
else:
    Self = "Symbol"


class Symbol(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.wrapped = False
        self.wrap_failed = False

    @property
    def exported(self) -> bool:
        """Returns whether the symbol is exported according to golang"""
        return self.name[0].isupper()

    def wrap(self, go_wrap_handler: GoWrapHandler):
        if self.wrapped:
            return
        return self._wrap(go_wrap_handler)

    @abstractmethod
    def _wrap(self, wh: GoWrapHandler):
        """
        Writes to a go file the wrapper, which allows exportation
        Sets afterward `wrapped` attribute to True
        """
        self.wrapped = True

    @classmethod
    @abstractmethod
    def from_match(cls, m: re.Match[str], other_symbols: dict[str, 'Symbol']) -> Self:
        if m.group(0).startswith('func'):
            return GoFunc.from_match(m=m, other_symbols=other_symbols)
        elif m.group(0).startswith('type'):
            return GoStruct.from_match(m=m, other_symbols=other_symbols)
        else:
            raise NotImplementedError

class GoFunc(Symbol):
    ...

class GoStruct(Symbol):
    ...