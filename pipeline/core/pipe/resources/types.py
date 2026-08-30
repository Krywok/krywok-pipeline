from __future__ import annotations

from functools import partial
from typing import Any, NotRequired, TypedDict

from pipeline.handlers.condition_handler.cls import ConditionHandler
from pipeline.handlers.match_handler.cls import MatchHandler
from pipeline.handlers.transform_handler.cls import TransformHandler

PipeConditions = dict[type[ConditionHandler] | partial[ConditionHandler], Any]
PipeMatches = dict[type[MatchHandler] | partial[MatchHandler], Any]
PipeTransform = dict[type[TransformHandler] | partial[TransformHandler], Any]

PipeContext = dict[str, Any]
PipeMetadata = dict[str, Any]


class _PipeBaseConfig(TypedDict):
    setup: NotRequired[PipeTransform]

    conditions: NotRequired[PipeConditions]
    matches: NotRequired[PipeMatches]
    transform: NotRequired[PipeTransform]

    optional: NotRequired[bool]

    metadata: NotRequired[PipeMetadata]


class PipeConfig(_PipeBaseConfig):
    type: type


class PipeUpdateConfig(_PipeBaseConfig):
    pass
