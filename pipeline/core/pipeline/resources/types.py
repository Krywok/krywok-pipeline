from typing import Any, Callable, Protocol

from pipeline.core.pipeline.resources.constants import PipelineHook
from pipeline.handlers.condition_handler.resources.types import ConditionErrors

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
