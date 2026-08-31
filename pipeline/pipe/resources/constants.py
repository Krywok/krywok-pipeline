from __future__ import annotations

from typing import Any, NamedTuple

from pipeline.handler.condition.resources.types import ConditionErrors


class PipeResult(NamedTuple):
    value: Any

    condition_errors: ConditionErrors
    match_errors: ConditionErrors
