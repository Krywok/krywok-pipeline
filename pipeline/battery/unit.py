from typing import Unpack

from pipeline.core.pipe.resources.types import PipeConfig, PipeUpdateConfig


class BatteryUnit:
    """
    A reusable container for a single pipe configuration.

    Stores a pre-defined set of pipe arguments that can be retrieved and optionally extended at
    the point of use via the `sink()` method.
    """
    def __init__(self, **pipe_config: Unpack[PipeConfig]) -> None:
        """
        Initializes the BatteryUnit with a fixed pipe configuration.

        Args:
            **pipe_config (PipeConfig): The pipe configuration to store.
        """
        self.pipe_config: PipeConfig = pipe_config

    def sink(self, **update: Unpack[PipeUpdateConfig]) -> PipeConfig:
        """
        Returns the stored pipe configuration, optionally merged with overrides.

        This method is the primary way to consume a BatteryUnit. It returns a
        `PipeConfig` dictionary ready to be passed to a `Pipe` or `Pipeline`.   
        Any keyword arguments provided in `update` will overwrite the
        corresponding keys in the stored configuration, allowing for
        field-specific customization without modifying the original unit.

        Args:
            **update (PipeUpdateConfig): Optional overrides to merge into the stored configuration.

        Returns:
            PipeConfig: A merged dictionary of the stored configuration and any provided overrides.
        """
        if update is None:
            return self.pipe_config

        return {**self.pipe_config, **update}
