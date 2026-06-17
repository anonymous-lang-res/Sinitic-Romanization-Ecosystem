"""Parse CantRomZJ1 text into PyCantonese-style objects."""

from __future__ import annotations

from pycantonese.jyutping import Jyutping


def parse_cantromzj1(text: str) -> list[Jyutping]:
    """
    Parse concatenated or space-separated CantRomZJ1 text.

    This file is self-contained and does not import any other project file.

    Example:
        parse_cantromzj1("heong1A|55gong2A|35")
        -> [Jyutping(onset='h', nucleus='eo', coda='ng', tone='1A|55'),
            Jyutping(onset='g', nucleus='o', coda='ng', tone='2A|35')]
    """
    tones = (
        "4Aa|5",
        "4Ab|3",
        "1A|55",
        "1B|21",
        "2A|35",
        "2B|13",
        "3A|33",
        "3B|22",
        "4B|2",
    )
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

    def parse_syllable(syllable: str) -> Jyutping:
        syllable = syllable.strip()
        body = ""
        tone = ""

        for candidate in tones:
            if syllable.endswith(candidate):
                body = syllable[:-len(candidate)]
                tone = candidate
                break

        if not tone:
            raise ValueError(
                f"Cannot find a valid CantRomZJ1 tone suffix in {syllable!r}"
            )
        if not body:
            raise ValueError(f"Missing segmental body before tone in {syllable!r}")

        if body in {"m", "ng"}:
            return Jyutping(onset="", nucleus=body, coda="", tone=tone)

        for onset in onsets:
            if onset and not body.startswith(onset):
                continue

            rest = body[len(onset):] if onset else body
            if not rest:
                continue

            for coda in codas:
                if coda and not rest.endswith(coda):
                    continue

                nucleus = rest[:-len(coda)] if coda else rest
                if nucleus in valid_nuclei:
                    return Jyutping(
                        onset=onset,
                        nucleus=nucleus,
                        coda=coda,
                        tone=tone,
                    )

        raise ValueError(f"Cannot split CantRomZJ1 syllable body {body!r}")

    return [parse_syllable(syllable) for syllable in split_syllables(text)]
