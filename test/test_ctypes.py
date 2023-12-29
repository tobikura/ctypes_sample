import pytest
import ctypes
from pathlib import Path
import numpy as np
import math


def test_find_library() -> None:
    import ctypes_sample as cs

    lib_path = cs.find_library("sample", Path(cs.__file__).parent)
    print(f"\nlib_path={lib_path}")
    assert lib_path is not None
    lib = ctypes.cdll.LoadLibrary(str(lib_path))
    assert lib.add_scaler(1, 2) == 3


def test_load_module() -> None:
    import ctypes_sample as cs
    from ctypes_sample import ctypes_sample

    print(f"x={dir(ctypes_sample)}")
    print(f"x={dir(cs.ctypes_sample.sample)}")
    assert isinstance(cs.sample, cs.CModule)


def test_add() -> None:
    import ctypes_sample as cs

    assert cs.sample.add_scaler(1, 2) == 3


def test_copy_int_normal() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.int32)
    b = np.zeros_like(a)
    cs.sample.cdll.copy_int(
        b.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), a.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)), len(a)
    )
    print(f"dst={b}")
    assert np.all(b == a)

    b = np.zeros_like(a)
    cs.sample.copy_int(b, a, len(a))
    print(f"dst={b}")
    assert np.all(b == a)


def test_copy_int_view() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.int32)[1:3]
    b = np.zeros_like(a)
    cs.sample.copy_int(b, a, len(a))
    print(f"dst={b}")
    assert np.all(b == a)

    a = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]], dtype=np.int32)[1, :]
    b = np.zeros_like(a)
    cs.sample.copy_int(b, a, len(a))
    print(f"dst={b}")
    assert np.all(b == a)

    a0 = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]], dtype=np.int32)
    b = np.zeros([12], dtype=np.int32)
    cs.sample.copy_int(b[6:], a0[0, :], len(a0[0, :]))
    cs.sample.copy_int(b[:6], a0[1, :], len(a0[1, :]))
    print(f"dst={b}")
    expected_b = np.zeros([12], dtype=np.int32)
    expected_b[6:] = a0[0, :]
    expected_b[:6] = a0[1, :]
    assert np.all(b == expected_b)


def test_copy_int_not_c_contiguous() -> None:
    import ctypes_sample as cs

    a = np.flip(np.array([1, 2, 3, 4, 5, 6], dtype=np.int32))
    b = np.zeros_like(a)
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.copy_int(b, a, len(a))

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.int32)
    b = np.flip(np.zeros_like(a))
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.copy_int(b, a, len(a))


def test_add_int() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.int32)
    b = np.array([7, 8, 9, 10, 11, 12], dtype=np.int32)
    x = np.zeros_like(a)
    cs.sample.add_int(x, b, a, len(a))
    print(f"dst={x}")
    assert np.all(x == (a + b))

    a2 = np.flip(a)
    x = np.zeros_like(a)
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.add_int(x, b, a2, len(a2))

    x = np.flip(np.zeros_like(a))
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.add_int(x, b, a2, len(a2))


def test_mul_int() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.int32)
    b = np.array([7, 8, 9, 10, 11, 12], dtype=np.int32)
    x = np.zeros_like(a)
    cs.sample.mul_int(x, b, a, len(a))
    print(f"dst={x}")
    assert np.all(x == (a * b))

    a2 = np.flip(a)
    x = np.zeros_like(a)
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.mul_int(x, b, a2, len(a2))

    x = np.flip(np.zeros_like(a))
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.mul_int(x, b, a2, len(a2))


def test_sum_int() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.int32)
    x = cs.sample.sum_int(a, len(a))
    print(f"dst={x}")
    assert np.all(x == np.sum(a))

    a2 = np.flip(a)
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        x = cs.sample.sum_int(a2, len(a2))


def test_copy_float_normal() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.float32)
    b = np.zeros_like(a)
    cs.sample.cdll.copy_float(
        b.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), a.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), len(a)
    )
    print(f"dst={b}")
    assert np.all(b == a)

    b = np.zeros_like(a)
    cs.sample.copy_float(b, a, len(a))
    print(f"dst={b}")
    assert np.all(b == a)


def test_copy_float_view() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.float32)[1:3]
    b = np.zeros_like(a)
    cs.sample.copy_float(b, a, len(a))
    print(f"dst={b}")
    assert np.all(b == a)

    a = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]], dtype=np.float32)[1, :]
    b = np.zeros_like(a)
    cs.sample.copy_float(b, a, len(a))
    print(f"dst={b}")
    assert np.all(b == a)

    a0 = np.array([[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]], dtype=np.float32)
    b = np.zeros([12], dtype=np.float32)
    cs.sample.copy_float(b[6:], a0[0, :], len(a0[0, :]))
    cs.sample.copy_float(b[:6], a0[1, :], len(a0[1, :]))
    print(f"dst={b}")
    expected_b = np.zeros([12], dtype=np.float32)
    expected_b[6:] = a0[0, :]
    expected_b[:6] = a0[1, :]
    assert np.all(b == expected_b)


def test_copy_float_not_c_contiguous() -> None:
    import ctypes_sample as cs

    a = np.flip(np.array([1, 2, 3, 4, 5, 6], dtype=np.float32))
    b = np.zeros_like(a)
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.copy_float(b, a, len(a))

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.float32)
    b = np.flip(np.zeros_like(a))
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.copy_float(b, a, len(a))


def test_add_float() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.float32)
    b = np.array([7, 8, 9, 10, 11, 12], dtype=np.float32)
    x = np.zeros_like(a)
    cs.sample.add_float(x, b, a, len(a))
    print(f"dst={x}")
    assert np.all(x == (a + b))

    a2 = np.flip(a)
    x = np.zeros_like(a)
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.add_float(x, b, a2, len(a2))

    x = np.flip(np.zeros_like(a))
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.add_float(x, b, a2, len(a2))


def test_mul_float() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.float32)
    b = np.array([7, 8, 9, 10, 11, 12], dtype=np.float32)
    x = np.zeros_like(a)
    cs.sample.mul_float(x, b, a, len(a))
    print(f"dst={x}")
    assert np.all(x == (a * b))

    a2 = np.flip(a)
    x = np.zeros_like(a)
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.mul_float(x, b, a2, len(a2))

    x = np.flip(np.zeros_like(a))
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        cs.sample.mul_float(x, b, a2, len(a2))


def test_sum_float() -> None:
    import ctypes_sample as cs

    a = np.array([1, 2, 3, 4, 5, 6], dtype=np.float32)
    x = cs.sample.sum_float(a, len(a))
    print(f"dst={x}")
    assert np.all(x == np.sum(a))

    a2 = np.flip(a)
    with pytest.raises(ValueError, match=r"ndarray is not C-contiguous"):
        x = cs.sample.sum_float(a2, len(a2))


def test_init_struct() -> None:
    import ctypes_sample as cs

    s = cs.SampleStruct()
    cs.sample.init_struct(s)
    print(f"struct: a={s.a}, b={s.b}, c={s.c}, d={s.d}")
    assert s.a == 0x12345678
    assert s.b == 6
    assert math.isclose(s.c, 1.23, rel_tol=0.000001)
    assert math.isclose(s.d, 4.56, rel_tol=0.000001)


def test_print_struct() -> None:
    import ctypes_sample as cs

    s = cs.SampleStruct()
    s.a = 1
    s.b = 2
    s.c = 3.0
    s.d = 4.0
    cs.sample.print_struct(s)
