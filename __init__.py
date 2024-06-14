from typing import Dict, Any, Iterator, Optional 
from collections import abc
from types import FunctionType
import inspect

class DynamicScope(abc.Mapping):
    def __init__(self):
        self.env: Dict[str, Optional[Any]] = {}

    def __getitem__(self, key: str) -> Optional[Any]:
        return self.env.__getitem__(key)

    def __setitem__(self, key: str, value: Optional[Any]):
        self.env.__setitem__(key, value)

    def __delitem__(self, key: str):
        self.env.__delitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.env.__iter__()

    def __len__(self) -> int:
        return self.env.__len__()

def get_dynamic_re() -> DynamicScope:
    environment = DynamicScope()
    stack = inspect.stack()
    # for each record in the stack execute following
    for i in range(len(stack)):
        # skip itself
        if i == 0:
            continue
        # Saves "Frame Object" information
        fObject = stack[i][0]
        for variable in fObject.f_locals:
            # skipping instances of variable previously saved, null variables, and free variables
            if variable in environment.env or fObject.f_locals[variable] is None or variable in fObject.f_code.co_freevars:
                continue 
            environment[variable] = fObject.f_locals[variable]
    return environment
