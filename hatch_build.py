import sys
import sysconfig
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.builders.wheel import WheelBuilderConfig
from typing import Union, Any
import platform

darwin = platform.system() == "Darwin"
if darwin:
    from pathlib import Path
    from macholib import MachO, mach_o
    from macholib.ptypes import Structure
    from typing import Optional, Tuple, List

    def get_mach_o() -> Optional[MachO.MachO]:
        top_dir = Path(__file__).parent
        lib_path = top_dir / "ctypes_sample/libsample.dylib"
        if not lib_path.exists():
            return None
        return MachO.MachO(lib_path)

    def get_osx_cpu(o: MachO) -> List[str]:
        return [mach_o.CPU_TYPE_NAMES[h.header.cputype] for h in o.headers]

    def find_command(h: MachO.MachOHeader, cmd: int) -> Optional[Tuple[mach_o.load_command, Any, bytes]]:
        commands = list(filter(lambda c: c[0].cmd == cmd, h.commands))
        if len(commands) > 0:
            command = commands[0]
            assert isinstance(command, tuple)
            assert isinstance(command[0], mach_o.load_command)
            assert isinstance(command[1], Structure)
            assert isinstance(command[2], bytes)
            return (command[0], command[1], command[2])
        else:
            return None

    def find_build_version_command(h: MachO.MachOHeader) -> Optional[mach_o.build_version_command]:
        command = find_command(h, mach_o.LC_BUILD_VERSION)
        if command:
            return command[1]
        else:
            return None

    def mach_version_to_str(version: Any) -> str:
        v = mach_o.mach_version_helper(version)
        return f"{v.major}.{v.minor}"

    def get_osx_minos(o: MachO) -> List[str]:
        minos = []
        for h in o.headers:
            b = find_build_version_command(h)
            if b is None:
                continue
            minos.append(mach_version_to_str(b.minos))
        return minos


def normalize_platform_tag(platform: str) -> str:
    trans_tbl: dict[str, Union[str, int, None]] = {"-": "_", ".": "_"}
    return platform.translate(str.maketrans(trans_tbl))


class CustomBuildHook(BuildHookInterface[WheelBuilderConfig]):
    """Build hook."""

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        """Setup the build tag."""

        if self.target_name != "wheel":
            return

        python_tag = self.config.get("python_tag", f"cp{''.join([str(x) for x in sys.version_info[:2]])}")
        abi_tag = self.config.get("abi_tag", "none")

        if darwin:
            o = get_mach_o()
            assert o is not None
            minos = get_osx_minos(o)
            default_pf_tag = normalize_platform_tag(f"macosx_{minos[0]}_universal2")
        else:
            default_pf_tag = normalize_platform_tag(sysconfig.get_platform())
        platform_tag = self.config.get("platform_tag", default_pf_tag)
        build_data["tag"] = f"{python_tag}-{abi_tag}-{platform_tag}"
