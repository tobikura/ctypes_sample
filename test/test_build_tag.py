import pytest
import sys
import sysconfig
import platform
from pip._internal.utils.compatibility_tags import get_supported
from pip._vendor.packaging.tags import platform_tags, compatible_tags
from hatchling.metadata.core import ProjectMetadata
from typing import Any
import hatch_build
import re


def test_python_version_info() -> None:
    print()
    print(f"platform.system(): {platform.system()}")
    print(f"sys.version_info: {sys.version_info}")
    print(f"sysconfig.get_platform(): {sysconfig.get_platform()}")


def test_pip_list_supported_tag() -> None:
    print()
    abis = []
    interpreters = []
    platforms = []

    print("Support TAGS:")
    for p in get_supported():
        print(f"  {p}")
        if p.abi not in abis:
            abis.append(p.abi)
        if p.interpreter not in interpreters:
            interpreters.append(p.interpreter)
        if p.platform not in platforms:
            platforms.append(p.platform)
    print()

    print("Support ABI:")
    for abi in abis:
        print(f"  {abi}")
    print()
    print("Support interpreter:")
    for interpreter in interpreters:
        print(f"  {interpreter}")
    print()
    print("Support platform:")
    for pf in platforms:
        print(f"  {pf}")
    print()


def test_pip_list_compatible_tags() -> None:
    for x in platform_tags():
        print(f"platform_tags: {x}")
    for y in compatible_tags(python_version=sys.version_info[:2], interpreter="cp"):
        print(f"compatible_tags: {y}")


def test_build_tag() -> None:
    build_data: dict[str, Any] = {}
    hook = hatch_build.CustomBuildHook(
        "dummy_root",
        {},
        None,  # type: ignore
        ProjectMetadata("dummy_root", None),
        "dummy_dir",
        "wheel",
        None,
    )
    hook.initialize("0.0.1", build_data)
    print()
    print(f"build tag: {build_data['tag']}")
    supported = build_data["tag"] in map(str, get_supported())
    print(f"supported: {supported}")
    assert supported is True


@pytest.mark.skipif(platform.system() != "Darwin", reason="This platform is not Darwin")
def test_osx_cpu() -> None:
    print()
    o = hatch_build.get_mach_o()
    assert o is not None

    cpu = hatch_build.get_osx_cpu(o)

    print(f"arch: {', '.join(cpu)}")
    assert "x86_64" in cpu
    assert "ARM64" in cpu


@pytest.mark.skipif(platform.system() != "Darwin", reason="This platform is not Darwin")
def test_osx_minos() -> None:
    print()
    o = hatch_build.get_mach_o()
    assert o is not None

    cpu = hatch_build.get_osx_cpu(o)
    minos = hatch_build.get_osx_minos(o)

    assert len(cpu) == len(minos)
    for i in range(len(cpu)):
        print(f"arch: {cpu[i]}, minos: {minos[i]}")
        assert re.match(r"\d+\.\d+", minos[i])


@pytest.mark.skipif(platform.system() != "Darwin", reason="This platform is not Darwin")
def test_osx_otool_print_load_command_shared_lib() -> None:
    from pathlib import Path
    import subprocess

    top_dir = Path(__file__).parent.parent
    lib_path = top_dir / "ctypes_sample/libsample.dylib"
    if not lib_path.exists():
        return None

    proc = subprocess.run(f"otool -l {lib_path}", shell=True, text=True)
