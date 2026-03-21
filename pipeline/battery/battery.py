from typing import Unpack

from pipeline import Condition, Match
from pipeline.battery.unit import BatteryUnit
from pipeline.core.pipe.resources.types import PipeConfig


class Battery:
    UUID = BatteryUnit(
        type=str,
        conditions={Condition.ExactLength: 36},
        matches={Match.Format.UUID: None}
    )

    @classmethod
    def add(cls, name: str, **pipe_config: Unpack[PipeConfig]) -> None:
        setattr(cls, name, BatteryUnit(**pipe_config))

    @classmethod
    def get(cls, name: str) -> BatteryUnit:
        return getattr(cls, name)

    @staticmethod
    def use_email(min_length: int = 6, max_length: int = 64) -> BatteryUnit:
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
        return BatteryUnit(
            type=int,
            conditions={
                Condition.MinNumber: min_number,
                Condition.MaxNumber: max_number
            }
        )

    @staticmethod
    def use_offset(min_number: int = 0, max_number: int = 1000) -> BatteryUnit:
        return BatteryUnit(
            type=int,
            conditions={
                Condition.MinNumber: min_number,
                Condition.MaxNumber: max_number
            }
        )
