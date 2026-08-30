from __future__ import annotations

from typing import ClassVar

from pipeline.handlers.match_handler.units.match_encoding import MatchEncoding
from pipeline.handlers.match_handler.units.match_format import MatchFormat
from pipeline.handlers.match_handler.units.match_localization import \
    MatchLocalization
from pipeline.handlers.match_handler.units.match_network import MatchNetwork
from pipeline.handlers.match_handler.units.match_regex import MatchRegex
from pipeline.handlers.match_handler.units.match_text import MatchText
from pipeline.handlers.match_handler.units.match_time import MatchTime
from pipeline.handlers.match_handler.units.match_web import MatchWeb


class Match:
    """
    Central registry for all match handler units.

    This class provides a convenient way to access different match handlers
    (e.g., Text, Regex, Web) from a single location.
    """
    Text: ClassVar = MatchText
    Regex: ClassVar = MatchRegex

    Web: ClassVar = MatchWeb
    Network: ClassVar = MatchNetwork

    Time: ClassVar = MatchTime
    Localization: ClassVar = MatchLocalization

    Format: ClassVar = MatchFormat
    Encoding: ClassVar = MatchEncoding
