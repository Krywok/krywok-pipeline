from collections.abc import Callable
from typing import Any, Protocol

from pipeline.handler.condition.resources.types import ConditionErrors
from pipeline.pipeline.resources.constants import PipelineHook

PipelineErrors = dict[str, ConditionErrors]
PipelineHookFunc = Callable[[PipelineHook], None]
PipelineTeardownFunc = Callable[[Any], None]
PipelineHandleErrorsFunc = Callable[[PipelineErrors], None]


class PipelineHookValue(Protocol):
    @property
    def get(self) -> Any:
        ...

    def set(self, new_value: Any) -> Any:
        ...
