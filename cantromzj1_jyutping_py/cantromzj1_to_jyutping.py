"""Convert CantRomZJ1 text to Jyutping text."""

from __future__ import annotations

from typing import Literal


def cantromzj1_to_jyutping(
    cantromzj1: str,
    *,
    output_separator: str = "",
    return_mode: Literal["tuple", "string", "list"] = "tuple",
) -> str | list[str] | tuple[str, list[str]]:
    """
    Convert concatenated or space-separated CantRomZJ1 text to Jyutping.

    This file is self-contained and does not import any other project file.

    Args:
        cantromzj1: CantRomZJ1 text.
        output_separator: Separator used to join converted syllables.
        return_mode: ``"tuple"`` returns ``(joined, syllables)``;
            ``"string"`` returns only the joined string; ``"list"`` returns
            only the syllable list.

    Example:
        cantromzj1_to_jyutping("heong1A|55gong2A|35")
        -> ("hoeng1gong2", ["hoeng1", "gong2"])
    """
    tones_to_jyutping = {
        "1A|55": "1",
        "1B|21": "4",
        "2A|35": "2",
        "2B|13": "5",
        "3A|33": "3",
        "3B|22": "6",
        "4Aa|5": "1",
        "4Ab|3": "3",
        "4B|2": "6",
    }
    tones = tuple(sorted(tones_to_jyutping, key=len, reverse=True))
    nucleus_map = {
        "a": "aa",
        "e": "a",
        "ea": "e",
        "eo": "oe",
        "oe": "eo",
    }
    onsets = (
        "gw", "kw", "ng",
        "b", "p", "m", "f",
        "d", "t", "n", "l",
        "g", "k", "h",
        "w", "z", "c", "s", "j",
        "",
    )
    codas = ("ng", "p", "t", "k", "m", "n", "i", "u", "")
    valid_nuclei = {"a", "e", "ea", "i", "o", "u", "eo", "oe", "yu", "m", "ng"}

    def split_syllables(value: str) -> list[str]:
        value = value.strip()
        if not value:
            return []
        if " " in value:
            return [item for item in value.split() if item]

        syllables: list[str] = []
        start = 0
        i = 0

        while i < len(value):
            matched_tone = ""
            for candidate in tones:
                if value.startswith(candidate, i):
                    matched_tone = candidate
                    break

            if not matched_tone:
                i += 1
                continue

            end = i + len(matched_tone)
            syllables.append(value[start:end])
            start = end
            i = end

        if start != len(value):
            raise ValueError(
                f"Unparsed trailing content in CantRomZJ1 string: {value[start:]!r}"
            )

        return syllables

    def convert_syllable(syllable: str) -> str:
        syllable = syllable.strip()
        body = ""
        cantromzj1_tone = ""

        for candidate in tones:
            if syllable.endswith(candidate):
                body = syllable[:-len(candidate)]
                cantromzj1_tone = candidate
                break

        if not cantromzj1_tone:
            raise ValueError(
                f"Cannot find a valid CantRomZJ1 tone suffix in {syllable!r}"
            )
        if not body:
            raise ValueError(f"Missing segmental body before tone in {syllable!r}")

        onset = ""
        nucleus = ""
        coda = ""

        if body in {"m", "ng"}:
            nucleus = body
        else:
            matched = False
            for candidate_onset in onsets:
                if candidate_onset and not body.startswith(candidate_onset):
                    continue

                rest = body[len(candidate_onset):] if candidate_onset else body
                if not rest:
                    continue

                for candidate_coda in codas:
                    if candidate_coda and not rest.endswith(candidate_coda):
                        continue

                    candidate_nucleus = (
                        rest[:-len(candidate_coda)] if candidate_coda else rest
                    )
                    if candidate_nucleus in valid_nuclei:
                        onset = candidate_onset
                        nucleus = candidate_nucleus
                        coda = candidate_coda
                        matched = True
                        break

                if matched:
                    break

            if not matched:
                raise ValueError(f"Cannot split CantRomZJ1 syllable body {body!r}")

        try:
            tone = tones_to_jyutping[cantromzj1_tone]
        except KeyError as exc:
            raise ValueError(
                f"Unsupported CantRomZJ1 tone {cantromzj1_tone!r}"
            ) from exc

        jyutping_nucleus = nucleus_map.get(nucleus, nucleus)
        return f"{onset}{jyutping_nucleus}{coda}{tone}"

    converted = [convert_syllable(item) for item in split_syllables(cantromzj1)]
    joined = output_separator.join(converted)

    if return_mode == "tuple":
        return joined, converted
    if return_mode == "string":
        return joined
    if return_mode == "list":
        return converted

    raise ValueError("return_mode must be one of: 'tuple', 'string', 'list'")
