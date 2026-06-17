"""Convert one Jyutping syllable to one CantRomZJ1 syllable."""

from __future__ import annotations

import pycantonese


def jyutping_syllable_to_cantromzj1(jyutping_syllable: str) -> str:
    """
    Convert exactly one Jyutping syllable to a CantRomZJ1 syllable string.

    This file is self-contained and does not import any other project file.

    Example:
        jyutping_syllable_to_cantromzj1("hoeng1") -> "heong1A|55"
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

    parsed_items = pycantonese.parse_jyutping(jyutping_syllable.strip())
    if len(parsed_items) != 1:
        raise ValueError(
            f"Expected exactly one Jyutping syllable, got {len(parsed_items)}: "
            f"{jyutping_syllable!r}"
        )

    item = parsed_items[0]
    nucleus = nucleus_map.get(item.nucleus, item.nucleus)
    tone_map = checked_tone_map if item.coda in checked_codas else open_tone_map

    try:
        tone = tone_map[item.tone]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported Jyutping tone {item.tone!r} for coda {item.coda!r}"
        ) from exc

    return f"{item.onset}{nucleus}{item.coda}{tone}"