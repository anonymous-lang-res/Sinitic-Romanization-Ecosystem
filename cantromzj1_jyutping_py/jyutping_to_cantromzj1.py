"""Convert Jyutping text to CantRomZJ1 text."""

from __future__ import annotations

from typing import Literal

import pycantonese


def jyutping_to_cantromzj1(
    jyutping: str,
    *,
    output_separator: str = "",
    return_mode: Literal["tuple", "string", "list"] = "tuple",
) -> str | list[str] | tuple[str, list[str]]:
    """
    Convert a Jyutping string to CantRomZJ1.

    This file is self-contained and does not import any other project file.
    Concatenated and space-separated input are both accepted.

    Args:
        jyutping: Jyutping text such as ``"hoeng1gong2"`` or
            ``"hoeng1 gong2"``.
        output_separator: Separator used to join converted syllables.
        return_mode: ``"tuple"`` returns ``(joined, syllables)``;
            ``"string"`` returns only the joined string; ``"list"`` returns
            only the syllable list.

    Example:
        jyutping_to_cantromzj1("hoeng1gong2")
        -> ("heong1A|55gong2A|35", ["heong1A|55", "gong2A|35"])
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
    converted: list[str] = []

    for item in parsed_items:
        nucleus = nucleus_map.get(item.nucleus, item.nucleus)
        tone_map = checked_tone_map if item.coda in checked_codas else open_tone_map
        try:
            tone = tone_map[item.tone]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported Jyutping tone {item.tone!r} for coda {item.coda!r}"
            ) from exc

        converted.append(f"{item.onset}{nucleus}{item.coda}{tone}")

    joined = output_separator.join(converted)

    if return_mode == "tuple":
        return joined, converted
    if return_mode == "string":
        return joined
    if return_mode == "list":
        return converted

    raise ValueError("return_mode must be one of: 'tuple', 'string', 'list'")
