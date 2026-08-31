from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from pipeline.handler.base.resources.constants import HandlerMode

if TYPE_CHECKING:
    from pipeline.handler.condition.cls import ConditionHandler

ConditionError = Any
ConditionErrors = list[ConditionError]

ConditionErrorTemplate = Callable[['ConditionHandler'], Any]
ConditionErrorTemplates = dict[HandlerMode, ConditionErrorTemplate]
