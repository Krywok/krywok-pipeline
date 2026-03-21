from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from pipeline.core.pipe.resources.types import PipeConfig
    from pipeline.core.pipeline.resources.types import (
        PipelineErrors, PipelineHookValue
    )


@dataclass
class PipelineHook:
    field: Any

    value: PipelineHookValue

    is_valid: bool | None

    pipe_config: PipeConfig


class PipelineResult(NamedTuple):
    errors: PipelineErrors | None

    processed_data: dict | None
