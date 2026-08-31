from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pipeline.handlers.base.resources.constants import HandlerMode

if TYPE_CHECKING:
    from pipeline.handlers.base.cls import BaseHandler


class HandlerException(Exception):
    @staticmethod
    def _format_expected_type(expected_type: Any, /) -> str:
        if isinstance(expected_type, (tuple, list)):
            return ", ".join(
                HandlerException._format_expected_type(x) for x in expected_type
            )

        return getattr(expected_type, "__name__", str(expected_type))


class HandlerInvalidValueType(HandlerException):
    def __init__(self, handler: BaseHandler) -> None:
        error: str = (
            f"Value type mismatch in handler {handler.__class__}. "
            f"Expected type(s): {self._format_expected_type(handler._expected_type.value)}. "
            f"Received type: {type(handler.value).__name__}. "
            f"Value: {repr(handler.value)}."
        )

        super().__init__(error)


class HandlerInvalidPreferredValueType(HandlerException):
    def __init__(self, handler: BaseHandler) -> None:
        if not handler._preferred_value_type:
            raise HandlerException("No preferred value type.")

        error: str = (
            f"Preferred value type mismatch in handler {handler.__class__}. "
            f"Expected type(s): {self._format_expected_type(handler._raw_expected_type.value)}. "
            f"Received type: {handler._preferred_value_type.__name__}. "
        )

        super().__init__(error)


class HandlerInvalidArgumentType(HandlerException):
    def __init__(self, handler: BaseHandler) -> None:
        error: str = (
            f"Argument type mismatch in handler {handler.__class__}. "
            f"Expected type(s): {self._format_expected_type(handler._expected_type.argument)}. "
            f"Received type: {type(handler.argument).__name__}. "
            f"Value: {repr(handler.value)}. "
            f"Argument: {repr(handler.argument)}."
        )

        super().__init__(error)


class HandlerModeException(HandlerException):
    pass


class HandlerModeUnsupported(HandlerModeException):
    def __init__(self, handler_mode: HandlerMode) -> None:
        error: str = f"This handler does not support \"{handler_mode.value}\" mode."

        super().__init__(error)


class HandlerModeMissingContextValue(HandlerModeException):
    def __init__(self, argument: str) -> None:
        error: str = f"Hnadler mode is context, but there is missing context value for specifed context key \"{argument}\"."

        super().__init__(error)
