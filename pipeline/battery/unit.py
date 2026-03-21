from typing import Unpack

from pipeline.core.pipe.resources.types import PipeConfig, PipeUpdateConfig


class BatteryUnit:
    def __init__(self, **pipe_config: Unpack[PipeConfig]) -> None:
        self.pipe_config: PipeConfig = pipe_config

    def sink(self, **update: Unpack[PipeUpdateConfig]) -> PipeConfig:
        if update is None:
            return self.pipe_config

        return {**self.pipe_config, **update}
