from __future__ import annotations

from pipeline.handlers.base_handler.resources.constants import HandlerMode
from pipeline.handlers.match_handler.match_handler import MatchHandler


class MatchText:
    """
    Registry for text-related match handlers.

    Includes handlers for Lowercase, Uppercase, Digits, etc.
    """
    class Lowercase(MatchHandler[str, set | None]):
        """Accepts ONLY lowercase English letters (a-z) if no diacritics are provided via set."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only lowercase letters (a-z) and allowed diacritics."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument, "lower")

            return self.fullmatch(rf"^[a-z{diacritics}]+$")

    class LowercaseWithSpaces(MatchHandler[str, set | None]):
        """Accepts lowercase English letters (a-z) and spaces if no diacritics are provided via set."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only lowercase letters, spaces and allowed diacritics."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument, "lower")

            return self.fullmatch(rf"^[a-z {diacritics}]+$")

    class Uppercase(MatchHandler[str, set | None]):
        """Accepts ONLY uppercase English letters (A-Z) if no diacritics are provided via set."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only uppercase letters (A-Z) and allowed diacritics."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument, "upper")

            return self.fullmatch(rf"^[A-Z{diacritics}]+$")

    class UppercaseWithSpaces(MatchHandler[str, set | None]):
        """Accepts uppercase English letters (A-Z) and spaces if no diacritics are provided via set."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only uppercase letters, spaces and allowed diacritics."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument, "upper")

            return self.fullmatch(rf"^[A-Z {diacritics}]+$")

    class Letters(MatchHandler[str, set | None]):
        """Accepts ONLY English letters (a-z, A-Z) if no diacritics are provided via set."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only letters (a-z, A-Z) and allowed diacritics."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument)

            return self.fullmatch(rf"^[a-zA-Z{diacritics}]+$")

    class LettersWithSpaces(MatchHandler[str, set | None]):
        """Accepts English letters (a-z, A-Z) and spaces if no diacritics are provided via set."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only letters, spaces and allowed diacritics."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument)

            return self.fullmatch(rf"^[a-zA-Z {diacritics}]+$")

    class Digits(MatchHandler[str, None]):
        """Accepts ONLY numeric digits (0-9)"""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT: lambda _: "Must contain only digits (0-9)."
        }

        def query(self):
            return self.fullmatch(r"^\d+$")

    class DigitsWithSpaces(MatchHandler[str, None]):
        """Accepts numeric digits (0-9) and spaces"""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only digits and spaces (e.g., '123 456')."
        }

        def query(self):
            return self.fullmatch(r"^[\d ]+$")

    class Alphanumeric(MatchHandler[str, set | None]):
        """Accepts letters and digits if no diacritics are provided via set. No symbols or spaces."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only letters, digits and allowed diacritics."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument)

            return self.fullmatch(rf"^[a-zA-Z0-9{diacritics}]+$")

    class AlphanumericWithSpaces(MatchHandler[str, set | None]):
        """Accepts letters, digits, and spaces if no diacritics are provided via set. No symbols."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only letters, digits, spaces and allowed diacritics."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument)

            return self.fullmatch(rf"^[a-zA-Z0-9 {diacritics}]+$")

    class Printable(MatchHandler[str, set | None]):
        """Accepts ASCII (20-7E) and diacritics if provided via set."""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Contains invalid characters. Only printable ASCII and allowed diacritics are allowed."
        }

        def query(self):
            diacritics: str = self.get_diacritics(self.argument)

            return self.fullmatch(rf"^[ -~{diacritics}]+$")

    class NoWhitespace(MatchHandler[str, None]):
        """Ensures string contains no spaces, tabs, or line breaks"""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _: "Must not contain spaces, tabs, or line breaks."
        }

        def query(self):
            return not self.search(r"\s")

    class Slug(MatchHandler[str, None]):
        """URL-friendly strings: 'my-cool-post-123'"""
        SUPPORT = (HandlerMode.ROOT, HandlerMode.ITEM)

        ERROR_TEMPLATES = {
            HandlerMode.ROOT:
                lambda _:
                "Must contain only lowercase letters, numbers, and hyphens (e.g., 'my-post-123')."
        }

        def query(self):
            return self.fullmatch(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
