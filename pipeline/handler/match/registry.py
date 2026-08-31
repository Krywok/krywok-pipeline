from __future__ import annotations

from typing import ClassVar

from pipeline.handler.match.units.encoding import MatchEncoding
from pipeline.handler.match.units.format import MatchFormat
from pipeline.handler.match.units.localization import MatchLocalization
from pipeline.handler.match.units.network import MatchNetwork
from pipeline.handler.match.units.regex import MatchRegex
from pipeline.handler.match.units.text import MatchText
from pipeline.handler.match.units.time import MatchTime
from pipeline.handler.match.units.web import MatchWeb


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
