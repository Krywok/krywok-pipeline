from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, ClassVar, cast

from pipeline.handler.base.cls import A, BaseHandler, V
from pipeline.handler.base.resources.constants import HandlerMode
from pipeline.handler.base.resources.exceptions import HandlerModeException
from pipeline.handler.condition.resources.exceptions import \
    ConditionMissingRootErrorMsg

if TYPE_CHECKING:
    from pipeline.handler.condition.resources.types import (
        ConditionError, ConditionErrorTemplates
    )
    from pipeline.pipe.resources.types import PipeContext, PipeMetadata


def default_error_builder(self: "ConditionHandler"):
    return {'id': self.id, 'msg': self.error_msg, 'value': self.value}


class ConditionHandler(BaseHandler[V, A]):
    """
    Abstract base class for specific condition implementations.

    This class provides the infrastructure for condition checking, including error message generation
    and support for different handling modes (ROOT, ITEM).
    It expects subclasses to implement the `query` method.
    """
    ERROR_BUILDER: ClassVar[Callable[['ConditionHandler'],
                                     ConditionError]] = default_error_builder

    ERROR_TEMPLATES: ClassVar[ConditionErrorTemplates]

    def __init__(
        self,
        value: V,
        argument: A,
        context: PipeContext | None = None,
        metadata: PipeMetadata | None = None,
        _mode: HandlerMode = HandlerMode.ROOT,
        _item_use_key: bool | None = False,
        _preferred_value_type: type | None = None
    ) -> None:
        """
        Initializes the ConditionHandler.
        
        It ensures that if ROOT mode is supported, a corresponding error template is present.
        """
        super().__init__(
            value, argument, context, metadata, _mode, _item_use_key,
            _preferred_value_type
        )

        if HandlerMode.ROOT in self.SUPPORT and HandlerMode.ROOT not in self.ERROR_TEMPLATES:
            raise ConditionMissingRootErrorMsg()

    @abstractmethod
    def query(self) -> bool:
        """
        Performs the condition check.

        Returns:
            bool: True if the condition is met, False otherwise.
        """
        ...

    def _handle(self) -> ConditionError | None:
        """
        Handles the condition check in ROOT or CONTEXT mode.

        Returns:
            ConditionError | None: An error object if the check fails, None otherwise.
        """
        if not self.query():
            return self.ERROR_BUILDER()

    def _handle_item_mode(self) -> dict[str | int, ConditionError] | None:
        """
        Handles the condition check in ITEM mode (for iterables).

        Iterates over the input value and applies the check to each item.

        Returns:
            dict[str | int, ConditionError] | None: A dictionary of errors keyed by item index/key,
            or None if no errors occurred.
        
        Raises:
            HandlerModeException: If the input value is not a supported iterable type.
        """
        errors = {}

        if isinstance(self.input_value, (list, tuple, set)):
            items = enumerate(self.input_value)
        elif isinstance(self.input_value, dict):
            items = self.input_value.items()
        else:
            raise HandlerModeException(
                "Cannot iterate over value. Expected a list, tuple, set, or dict."
            )

        for key, value in items:
            if self._item_use_key:
                value = key

            if not self._is_valid_type(value, self._expected_value_type):
                continue

            # NOTE: We use can cast() here because we checked if the value type is valid but linter does not know that.
            self.value = cast(V, value)

            self._item_index = key

            if not self.query():
                errors[key] = (self.ERROR_BUILDER())

        return errors if errors else None

    @property
    def error_msg(self) -> Any:
        """
        Generates the error message based on the current mode and error templates.

        Returns:
            Any: The generated error message.
        
        Raises:
            ConditionMissingRootErrorMsg: If the root error template is missing.
        """
        if self._mode in self.ERROR_TEMPLATES:
            return self.ERROR_TEMPLATES[self._mode](self)

        if HandlerMode.ROOT not in self.ERROR_TEMPLATES:
            raise ConditionMissingRootErrorMsg()

        return self.ERROR_TEMPLATES[HandlerMode.ROOT](self)
