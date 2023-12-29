import sys
import sysconfig
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.builders.wheel import WheelBuilderConfig
from typing import Union, Any


class CustomBuildHook(BuildHookInterface[WheelBuilderConfig]):
    """Build hook."""

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        """Setup the build tag."""

        if self.target_name != "wheel":
            return

        python_tag = self.config.get("python_tag", f"cp{''.join([str(x) for x in sys.version_info[:2]])}")
        abi_tag = self.config.get("abi_tag", "none")
        trans_tbl: dict[str, Union[str, int, None]] = {"-": "_", ".": "_"}
        platform_tag = self.config.get("platform_tag", sysconfig.get_platform().translate(str.maketrans(trans_tbl)))
        build_data["tag"] = f"{python_tag}-{abi_tag}-{platform_tag}"
