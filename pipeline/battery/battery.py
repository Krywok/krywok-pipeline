from typing import Literal, Unpack

from pipeline import Condition, Match
from pipeline.battery.unit import BatteryUnit
from pipeline.core.pipe.resources.types import PipeConfig


class Battery:
    """
    A centralized registry of reusable pipe configurations for DRY validation.

    Battery serves as a collection of pre-built `BatteryUnit` instances that
    represent common validation patterns (e.g., UUID, email, pagination limits).
    These units can be registered statically as class attributes or added
    dynamically at runtime, and then consumed anywhere in the application
    via the `sink()` method.
    """
    UUID = BatteryUnit(
        type=str,
        conditions={Condition.ExactLength: 36},
        matches={Match.Format.UUID: None}
    )
    """A pre-built unit that validates a UUID v4 string."""
    @classmethod
    def add(cls, name: str, **pipe_config: Unpack[PipeConfig]) -> None:
        """
        Registers a new BatteryUnit as a class attribute.

        Creates a `BatteryUnit` from the provided pipe configuration and
        assigns it to the class under the given name. This allows dynamically
        extending the Battery registry at application startup.

        Args:
            name (str): The attribute name under which the unit will be stored on the class.
            **pipe_config (PipeConfig): The pipe configuration for the new unit.
        """
        setattr(cls, name, BatteryUnit(**pipe_config))

    @classmethod
    def get(cls, name: str) -> BatteryUnit:
        """
        Retrieves a registered BatteryUnit by name.

        Args:
            name (str): The attribute name of the unit to retrieve.

        Returns:
            BatteryUnit: The BatteryUnit instance registered under the given name.

        Raises:
            AttributeError: If no unit with the given name has been registered on the class.
        """
        return getattr(cls, name)

    @staticmethod
    def use_email(min_length: int = 6, max_length: int = 64) -> BatteryUnit:
        """
        Creates a BatteryUnit for email address validation.

        Produces a unit that validates a string value as a well-formed email
        address within a configurable length range.

        Args:
            min_length (int): The minimum allowed length of the email address.
                Defaults to 6.
            max_length (int): The maximum allowed length of the email address.
                Defaults to 64.

        Returns:
            BatteryUnit: A unit for email validation.
        """
        return BatteryUnit(
            type=str,
            conditions={
                Condition.MinLength: min_length,
                Condition.MaxLength: max_length
            },
            matches={Match.Format.Email: None}
        )

    @staticmethod
    def use_limit(min_number: int = 1, max_number: int = 1000) -> BatteryUnit:
        """
        Creates a BatteryUnit for pagination limit validation.

        Produces a unit that validates an integer value representing the
        number of items to return per page, within a configurable range.

        Args:
            min_number (int): The minimum allowed limit value. Defaults to 1.
            max_number (int): The maximum allowed limit value. Defaults to 1000.

        Returns:
            BatteryUnit: A unit for pagination limit validation.
        """
        return BatteryUnit(
            type=int,
            conditions={
                Condition.MinNumber: min_number,
                Condition.MaxNumber: max_number
            }
        )

    @staticmethod
    def use_offset(min_number: int = 0, max_number: int = 1000) -> BatteryUnit:
        """
        Creates a BatteryUnit for pagination offset validation.

        Produces a unit that validates an integer value representing the
        starting position of a result set, within a configurable range.
        Differs from `use_limit` only in its default `min_number` of 0,
        which allows an offset of zero as a valid starting point.

        Args:
            min_number (int): The minimum allowed offset value. Defaults to 0.
            max_number (int): The maximum allowed offset value. Defaults to 1000.

        Returns:
            BatteryUnit: A unit for pagination offset validation.
        """
        return BatteryUnit(
            type=int,
            conditions={
                Condition.MinNumber: min_number,
                Condition.MaxNumber: max_number
            }
        )

    @staticmethod
    def use_token(
        exact_length: int = 32, digits_only: bool = False
    ) -> BatteryUnit:
        """
        Creates a BatteryUnit for token validation.

        Produces a unit that validates a string as a fixed-length token.
        Can be configured for alphanumeric characters or strictly digits.

        Args:
            exact_length (int): The required exact length of the token. 
                Defaults to 32.
            digits_only (bool): If True, validates using Match.Text.Digits.
                If False, validates using Match.Text.Alphanumeric. Defaults to False.

        Returns:
            BatteryUnit: A unit for token validation.
        """
        pattern = Match.Text.Digits if digits_only else Match.Text.Alphanumeric

        return BatteryUnit(
            type=str,
            conditions={Condition.ExactLength: exact_length},
            matches={pattern: None}
        )

    @staticmethod
    def use_password(
        policy: Literal["relaxed", "normal", "strict"] | None
    ) -> BatteryUnit:
        """
        Creates a BatteryUnit for password validation.

        Produces a unit that validates a string's length and, optionally, 
        its complexity against predefined security patterns.

        Args:
            policy (Literal["relaxed", "normal", "strict"]): The complexity level. If None, only
                length is validated (min: 6, max: 64).

        Returns:
            BatteryUnit: A unit for password validation.
        """
        config: PipeConfig = {
            'type': str,
            'conditions': {
                Condition.MinLength: 6,
                Condition.MaxLength: 64
            }
        }

        if policy is not None:
            config['matches'] = {Match.Format.Password: policy}

        return BatteryUnit(**config)
