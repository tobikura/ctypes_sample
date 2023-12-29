import ctypes
import platform
from pathlib import Path
import traceback
from typing import Optional, List, Dict, Callable, Iterable, Any
import numpy as np


class CModule:
    def __init__(self, name: str) -> None:
        self.cdll = load_library(name, base_dir=Path(__file__).parent)
        self.func_map: Dict[str, Callable[..., Any]] = {}

    def __getattr__(self, name: str) -> Any:
        if name in self.func_map:
            return self.func_map[name]
        raise AttributeError(f"'Sample' object has no attribute '{name}'")

    def register_function(
        self, func_name: str, restype: Optional[type], argtypes: Iterable[type], doc: str = ""
    ) -> None:
        func = getattr(self.cdll, func_name)
        func.restype = restype
        func.argtypes = argtypes
        if CModule.has_pointer_type(argtypes):
            self.func_map[func_name] = CModule.attach_np_args(func)
        else:
            if doc:
                func.__doc__ = doc
            self.func_map[func_name] = func

    @staticmethod
    def attach_np_args(func: Callable[..., Any]) -> Callable[..., Any]:
        def inner_func(*args: Any) -> Any:
            np_args = None
            for i in range(len(args)):
                if isinstance(args[i], np.ndarray):
                    if not args[i].flags["C_CONTIGUOUS"]:
                        raise ValueError("ndarray is not C-contiguous")
                    if np_args is None:
                        np_args = list(args)
                    np_args[i] = args[i].ctypes.data_as(ctypes.POINTER(_dtype_to_ctype(args[i].dtype)))
            if np_args:
                return func(*np_args)
            else:
                return func(*args)

        return inner_func

    @staticmethod
    def has_pointer_type(argtypes: Iterable[type]) -> bool:
        for typ in argtypes:
            if isinstance(typ, type(ctypes.POINTER(ctypes.c_int32))):
                return True
        return False


_dtype_to_ctype_map = {
    np.int64: ctypes.c_int64,
    np.int32: ctypes.c_int32,
    np.int16: ctypes.c_int16,
    np.int8: ctypes.c_int8,
    np.uint64: ctypes.c_uint64,
    np.uint32: ctypes.c_uint32,
    np.uint16: ctypes.c_uint16,
    np.uint8: ctypes.c_uint8,
    np.float64: ctypes.c_double,
    np.float32: ctypes.c_float,
}


def _dtype_to_ctype(dtype: np.dtype) -> type:
    for np_type, c_type in _dtype_to_ctype_map.items():
        if np.dtype(dtype) == np_type:
            return c_type
    raise RuntimeError(f"not support numpy.dtype ({dtype})")


def list_library_search_paths(name: str, base_dir: Path) -> List[Path]:
    pf = platform.system()
    if pf == "Windows":
        fmts = ["{}.dll", "{}"]
    elif pf == "Darwin":
        fmts = ["{}.dylib", "lib{}.dylib", "{}"]
    elif pf == "Linux":
        fmts = ["{}.so", "lib{}.so", "{}"]
    else:
        fmts = ["{}"]

    paths = []
    for fmt in fmts:
        paths.append(base_dir / fmt.format(name))
    return paths


def find_library(name: str, base_dir: Path) -> Optional[Path]:
    for path in list_library_search_paths(name, base_dir):
        if path.is_file():
            return path
    return None


def load_library(library_name: str, base_dir: Path = Path("")) -> ctypes.CDLL:
    lib_path = find_library(library_name, base_dir)
    if lib_path is not None:
        library_name = str(lib_path)
    return ctypes.cdll.LoadLibrary(library_name)


class SampleStruct(ctypes.Structure):
    _fields_ = [("a", ctypes.c_int32), ("b", ctypes.c_int32), ("c", ctypes.c_float), ("d", ctypes.c_float)]


def setup_sample_module() -> CModule:
    sample = CModule("sample")
    sample.register_function(
        "add_scaler", ctypes.c_int32, (ctypes.c_int32, ctypes.c_int32), doc="int add_scaler(int a, int b);"
    )
    sample.register_function(
        "copy_int",
        None,
        (ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.c_int32),
        doc="void copy_int(int *dst, int *src, int len);",
    )
    sample.register_function(
        "add_int",
        None,
        (
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.c_int32,
        ),
        doc="void add_int(int *dst, int *a, int *b, int len);",
    )
    sample.register_function(
        "mul_int",
        None,
        (
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.POINTER(ctypes.c_int32),
            ctypes.c_int32,
        ),
        doc="void mul_int(int *dst, int *a, int *b, int len);",
    )
    sample.register_function(
        "sum_int",
        ctypes.c_int32,
        (ctypes.POINTER(ctypes.c_int32), ctypes.c_int32),
        doc="int sum_int(int *a, int len);",
    )
    sample.register_function(
        "copy_float",
        None,
        (ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int32),
        doc="void copy_float(float *dst, float *src, int len);",
    )
    sample.register_function(
        "add_float",
        None,
        (
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.c_int32,
        ),
        doc="void add_float(float *dst, float *a, float *b, int len);",
    )
    sample.register_function(
        "mul_float",
        None,
        (
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.POINTER(ctypes.c_float),
            ctypes.c_int32,
        ),
        doc="void mul_float(float *dst, float *a, float *b, int len);",
    )
    sample.register_function(
        "sum_float",
        ctypes.c_float,
        (ctypes.POINTER(ctypes.c_float), ctypes.c_int32),
        doc="float sum_float(float *a, int len);",
    )
    sample.register_function(
        "init_struct", None, (ctypes.POINTER(SampleStruct),), doc="void init_struct(struct sample_struct *s);"
    )
    sample.register_function(
        "print_struct", None, (ctypes.POINTER(SampleStruct),), doc="void print_struct(struct sample_struct *s);"
    )

    return sample


try:
    sample = setup_sample_module()
except Exception as e:
    print(type(e))
    print(traceback.format_exc())
