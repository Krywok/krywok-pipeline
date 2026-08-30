from __future__ import annotations

from typing import TYPE_CHECKING, Any
from collections.abc import Callable

from pipeline.handlers.base_handler.resources.constants import HandlerMode

if TYPE_CHECKING:
    from pipeline.handlers.condition_handler.cls import ConditionHandler

ConditionError = Any
ConditionErrors = list[ConditionError]

ConditionErrorTemplate = Callable[['ConditionHandler'], Any]
ConditionErrorTemplates = dict[HandlerMode, ConditionErrorTemplate]
