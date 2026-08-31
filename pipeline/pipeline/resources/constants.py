from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from pipeline.pipe.resources.types import PipeConfig
    from pipeline.pipeline.resources.types import PipelineErrors


@dataclass
class PipelineHook:
    field: Any

    value: Any

    is_valid: bool | None

    pipe_config: PipeConfig


class PipelineResult(NamedTuple):
    errors: PipelineErrors | None

    processed_data: dict | None
