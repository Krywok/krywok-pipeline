from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from pipeline.pipe.resources.types import PipeConfig
    from pipeline.pipeline.resources.types import PipelineErrors


@dataclass
class PipelineHook:
    field: Any

    value: PipelineHookValue

    is_valid: bool | None

    pipe_config: PipeConfig


class PipelineHookValue:
    __slots__ = ("value", )

    def __init__(self, value: Any) -> None:
        self.value = value

    @property
    def get(self) -> Any:
        return self.value

    def set(self, new_value: Any) -> Any:
        self.value = new_value

        return self.value


class PipelineResult(NamedTuple):
    errors: PipelineErrors | None

    processed_data: dict | None
