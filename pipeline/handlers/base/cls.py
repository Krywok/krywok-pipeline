from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import cached_property
from types import get_original_bases
from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar, get_args

from pipeline.handlers.base.resources.constants import (Flag,
                                                        HandlerExpectedType,
                                                        HandlerMode)
from pipeline.handlers.base.resources.exceptions import (
    HandlerException, HandlerInvalidArgumentType,
    HandlerInvalidPreferredValueType, HandlerInvalidValueType,
    HandlerModeMissingContextValue, HandlerModeUnsupported)

if TYPE_CHECKING:
    from pipeline.pipe.resources.types import PipeContext, PipeMetadata

V = TypeVar('V')
A = TypeVar('A')


class BaseHandler(ABC, Generic[V, A]):
    """
    Abstract base class for all handlers in the pipeline.

    Handlers are the building blocks of the pipeline, responsible for processing values
    (validation, matching, transformation) based on provided arguments and context.
    They support different modes of operation to handle single values, items in a collection,
    or values dependent on other context fields.

    Attributes:
        FLAGS (ClassVar[tuple[Flag, ...]]): Flags acting as settings for the handler.
            Example: `ConditionFlag.BREAK_PIPE_LOOP_ON_ERROR` stops processing if the handler fails.
        SUPPORT (ClassVar[tuple[HandlerMode, ...]]): Supported handler modes.
            - `HandlerMode.ROOT`: The handler processes the value directly.
            - `HandlerMode.ITEM`: The handler processes each item in a list/dict.
            - `HandlerMode.CONTEXT`: The handler uses another field from the context as an argument.
        CONTEXT_ARGUMENT_BUILDER (ClassVar[Callable | None]): Helper to build arguments from context.
            Used in CONTEXT mode to transform the context value before using it as an argument.
    """
    FLAGS: ClassVar[tuple[Flag, ...]] = tuple()

    SUPPORT: ClassVar[tuple[HandlerMode, ...]] = tuple()

    CONTEXT_ARGUMENT_BUILDER: ClassVar[Callable[['BaseHandler', Any], Any] |
                                       None] = None

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
        Initializes the BaseHandler.

        Args:
            value (V): The value to process.
            argument (A): The argument for the handler.
            context (PipeContext | None): Additional context for the handler.
            metadata (PipeMetadata | None): Metadata about the pipe execution.
            _mode (HandlerMode): The mode in which the handler is operating.
            _item_use_key (bool | None): If True and in ITEM mode, the handler operates on the
                key of a dictionary item instead of the value.
            _preferred_value_type (type | None): Specific type to prefer/enforce during type validation.
        """
        self.value: V = value
        self.argument: A = argument

        self.input_value: V = value
        self.input_argument: A = argument

        self.context: PipeContext = context or {}
        self.metadata: PipeMetadata = metadata or {}

        self._mode: HandlerMode = _mode

        self._item_index: int | str | None = None
        self._item_use_key: bool | None = _item_use_key

        self._preferred_value_type: type | None = _preferred_value_type

        self._prepare_and_validate_handler()

    def __init_subclass__(cls) -> None:
        """
        Extracts expected runtime types from class generics and sets a unique handler ID.

        During subclass creation, this method:
        1. Extracts generic type arguments for `value` and `argument` from class definition,
           recursively unpacking them into tuples stored in `cls._raw_expected_type` for runtime type validation.
        2. Generates a `snake_case` identifier (`cls.id`) from the class name.
        """
        super().__init_subclass__()

        def _extract_types(arg: Any, is_top: bool = True) -> Any:
            args: tuple[Any, ...] = get_args(arg)

            if not args:
                return (arg, ) if is_top else arg

            return tuple(_extract_types(x, is_top=False) for x in args)

        value_type, argument_type = map(
            _extract_types, get_args(get_original_bases(cls)[0])
        )

        cls._raw_expected_type = HandlerExpectedType(
            value=value_type, argument=argument_type
        )

        partial_snake: str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)

        cls.id = re.sub('([a-z0-9])([A-Z])', r'\1_\2', partial_snake).lower()

    def handle(self) -> Any:
        """
        Executes the handler logic based on the current mode.

        It delegates to `_handle()` for ROOT and CONTEXT modes, and `_handle_item_mode()`
        for ITEM mode.

        Returns:
            Any: The result of the handling operation. The return type depends on the specific
            handler implementation (e.g., specific error type, boolean, or transformed value).

        Raises:
            HandlerException: If the handler mode is invalid.
        """
        if self._mode in (HandlerMode.ROOT, HandlerMode.CONTEXT):
            return self._handle()
        elif self._mode == HandlerMode.ITEM:
            return self._handle_item_mode()
        else:
            raise HandlerException("Invalid handler mode.")

    def _prepare_and_validate_handler(self) -> None:
        """
        Prepares the handler for the current mode and validates input types.

        This methods checks if the requested mode is supported, perpares the handler argument
        (especially for CONTEXT mode), and validates that value and argument types match
        expectations (generics).

        Raises:
            HandlerModeUnsupported: If the current mode is not supported by the handler.
        """
        if self._mode not in self.SUPPORT:
            raise HandlerModeUnsupported(handler_mode=self._mode)

        self._prepare_handler_for_mode()
        self._validate_type_if_possible()

    def _prepare_handler_for_mode(self) -> None:
        """
        Performs specific preparation steps based on the handler mode.
        
        For CONTEXT mode, it retrieves the argument from the context using the provided
        argument name (stored in `self.argument`). It also handles optional argument transformation
        via `CONTEXT_ARGUMENT_BUILDER`.
        """
        match self._mode:
            case HandlerMode.CONTEXT:
                context_value: Any = self.context.get(str(self.argument), None)

                if context_value is None:
                    raise HandlerModeMissingContextValue(
                        argument=str(self.argument)
                    )

                self.argument = self.CONTEXT_ARGUMENT_BUILDER(
                    context_value
                ) if self.CONTEXT_ARGUMENT_BUILDER else context_value

    def _is_valid_type(
        self, value: Any, expected_type: tuple[type, ...]
    ) -> bool:
        """
        Checks if a value matches the expected type(s).

        Args:
            value (Any): The value to check.
            expected_type (tuple[type, ...]): The expected type.

        Returns:
            bool: True if the value matches the expected type, False otherwise.
        """
        if Any in expected_type:
            return True

        return isinstance(value, expected_type)

    def _validate_type_if_possible(self) -> None:
        """
        Validates the types of the input value and argument against the class generics.

        This ensures type safety at runtime, verifying that the handler is being applied
        to compatible data.

        Value type is only verified for ROOT and CONTEXT modes. For ITEM mode, the handler
        must implement its own logic.

        Raises:
            HandlerInvalidValueType: If the value type is invalid.
            HandlerInvalidArgumentType: If the argument type is invalid.
        """
        if self._mode in (HandlerMode.ROOT, HandlerMode.CONTEXT):
            if not self._is_valid_type(self.value, self._expected_type.value):
                raise HandlerInvalidValueType(handler=self)

        if not self._is_valid_type(self.argument, self._expected_type.argument):
            raise HandlerInvalidArgumentType(handler=self)

    @abstractmethod
    def _handle(self) -> Any:
        """
        Abstract method to implement the main handling logic.
        """
        ...

    @abstractmethod
    def _handle_item_mode(self) -> Any:
        """
        Abstract method to implement the handling logic for ITEM mode.
        """
        ...

    @cached_property
    def _expected_type(self) -> HandlerExpectedType:
        """
        Resolves the final target runtime types for validating `self.value` and `self.argument`.

        Returns the default `_raw_expected_type` parsed during subclass creation. If an instance-level
        `_preferred_value_type` was provided, it verifies compatibility against the allowed generic
        types and narrows down the expected `value` type to the preferred one.

        Returns:
            HandlerExpectedType: Container holding the expected type tuple(s) for `value` and `argument`.

        Raises:
            HandlerInvalidPreferredValueType: If `_preferred_value_type` is not compatible with the handler.
        """
        if not self._preferred_value_type:
            return self._raw_expected_type

        if self._preferred_value_type not in self._raw_expected_type.value and Any not in self._raw_expected_type.value:
            raise HandlerInvalidPreferredValueType(self)

        return HandlerExpectedType(
            value=(self._preferred_value_type, ),
            argument=self._raw_expected_type.argument
        )
