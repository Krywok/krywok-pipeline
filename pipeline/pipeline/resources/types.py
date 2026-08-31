from collections.abc import Callable
from typing import Any

from pipeline.handlers.condition.resources.types import ConditionErrors
from pipeline.pipeline.resources.constants import PipelineHook

PipelineErrors = dict[str, ConditionErrors]
PipelineHookFunc = Callable[[PipelineHook], None]
PipelineTeardownFunc = Callable[[Any], None]
PipelineHandleErrorsFunc = Callable[[PipelineErrors], None]
