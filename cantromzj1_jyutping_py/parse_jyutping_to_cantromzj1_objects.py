"""Convert Jyutping text to PyCantonese-style CantRomZJ1 objects."""

from __future__ import annotations

import pycantonese
from pycantonese.jyutping import Jyutping


def parse_jyutping_to_cantromzj1_objects(jyutping: str) -> list[Jyutping]:
    """
    Convert a Jyutping string into PyCantonese ``Jyutping`` objects whose
    nucleus and tone fields use CantRomZJ1 notation.

    This file is self-contained and does not import any other project file.

    Example:
        parse_jyutping_to_cantromzj1_objects("hoeng1gong2")
        -> [Jyutping(onset='h', nucleus='eo', coda='ng', tone='1A|55'), ...]
    """
    nucleus_map = {
        "aa": "a",
        "a": "e",
        "e": "ea",
        "oe": "eo",
        "eo": "oe",
    }
    open_tone_map = {
        "1": "1A|55",
        "4": "1B|21",
        "2": "2A|35",
        "5": "2B|13",
        "3": "3A|33",
        "6": "3B|22",
    }
    checked_tone_map = {
        "1": "4Aa|5",
        "3": "4Ab|3",
        "6": "4B|2",
    }
    checked_codas = {"p", "t", "k"}

    parsed_items = pycantonese.parse_jyutping(jyutping.replace(" ", ""))
    converted: list[Jyutping] = []

    for item in parsed_items:
        nucleus = nucleus_map.get(item.nucleus, item.nucleus)
        tone_map = checked_tone_map if item.coda in checked_codas else open_tone_map
        try:
            tone = tone_map[item.tone]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported Jyutping tone {item.tone!r} for coda {item.coda!r}"
            ) from exc

        converted.append(
            Jyutping(
                onset=item.onset,
                nucleus=nucleus,
                coda=item.coda,
                tone=tone,
            )
        )

    return converted
