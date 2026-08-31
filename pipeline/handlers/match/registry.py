from __future__ import annotations

from typing import ClassVar

from pipeline.handlers.match.units.encoding import MatchEncoding
from pipeline.handlers.match.units.format import MatchFormat
from pipeline.handlers.match.units.localization import MatchLocalization
from pipeline.handlers.match.units.network import MatchNetwork
from pipeline.handlers.match.units.regex import MatchRegex
from pipeline.handlers.match.units.text import MatchText
from pipeline.handlers.match.units.time import MatchTime
from pipeline.handlers.match.units.web import MatchWeb


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
