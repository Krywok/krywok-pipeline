import re
from typing import Literal, Optional

from pipeline.handlers.base_handler.base_handler import A, V
from pipeline.handlers.condition_handler.condition_handler import \
    ConditionHandler
from pipeline.handlers.match_handler.units.resources.constants import ISO_639_1


class MatchHandler(ConditionHandler[V, A]):
    """
    Base class for match handlers.

    Match handlers extend condition handlers to provide specific matching capabilities,
    often involving regular expressions or patterns.
    """
    def search(
        self,
        pattern: str | re.Pattern,
        flag: Optional[re.RegexFlag] = None
    ) -> bool:
        """
        Searches for the pattern in the value.

        Args:
            pattern (str | re.Pattern): The regex pattern to search for.
            flag (Optional[re.RegexFlag]): Optional regex flags.

        Returns:
            bool: True if the pattern is found, False otherwise.
        """
        return re.search(pattern, str(self.value), flag or 0) is not None

    def fullmatch(
        self,
        pattern: str | re.Pattern,
        flag: Optional[re.RegexFlag] = None
    ) -> bool:
        """
        Checks if the entire value matches the pattern.

        Args:
            pattern (str | re.Pattern): The regex pattern to match against.
            flag (Optional[re.RegexFlag]): Optional regex flags.

        Returns:
            bool: True if the entire value matches the pattern, False otherwise.
        """
        return re.fullmatch(pattern, str(self.value), flag or 0) is not None

    @staticmethod
    def get_diacritics(
        languages: set[str] | None,
        letter_case: Literal["lower", "upper"] | None = None,
        /,
    ) -> str:
        """
        Retrieves a string of diacritic characters for the specified languages.

        Combines all unique diacritic marks associated with a given set of ISO 639-1
        language codes. The output can be filtered by letter case or return both
        cases by default.

        Args:
            languages: A set of ISO 639-1 language codes (e.g., {"fr", "de"}). 
                If None or empty, an empty string is returned.
            letter_case: The desired grammatical case for the diacritics. 
                Options are "lower", "upper", or None. If None, both cases 
                are returned. This is a positional-only argument.

        Returns:
            A string containing the concatenated diacritic characters for the 
            requested languages and case.
        """
        if not languages:
            return ""

        def transform(base: str) -> str:
            if letter_case == "lower":
                return base

            if letter_case == "upper":
                return base.upper()

            return base + base.upper()

        return "".join(transform(ISO_639_1[language]) for language in languages)
