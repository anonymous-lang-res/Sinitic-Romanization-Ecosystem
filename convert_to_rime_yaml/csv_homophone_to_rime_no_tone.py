#!/usr/bin/env python3
"""
Convert a PhonConvert homophone-character CSV table to a minimal Rime input method.

Input CSV format:
    Syllable/Combination,汉字
    ok4A|1,惡
    bok4A|1,博剝駁膊搏

By default, tone information is removed from input codes:
    ok4A|1  -> ok
    bok4A|1 -> bok
    heong1A|55 -> heong

Generated files:
    <schema_id>.schema.yaml
    <schema_id>.dict.yaml

The generated Rime schema is intentionally minimal: it only supports basic typing
from romanized code to Chinese characters, without reverse lookup, fuzzy spelling,
accent compatibility, or other advanced features.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Iterable


# Matches common final tone suffixes used in RomZJ-style notation:
#   4A|1, 4B|5, 1A|44, 4Aa|5, 4Ab|3, 1, 2, 3, ...
# It is anchored at the end so only the final tone part is removed.
TONE_SUFFIX_RE = re.compile(r"(?:[1-9][A-Za-z]{0,2}(?:\|\d{1,2})?|[1-9])$")


def strip_tone(code: str) -> str:
    """Remove final tone notation from one romanized syllable/code."""
    code = code.strip()
    code = TONE_SUFFIX_RE.sub("", code)
    return code


def normalize_code(code: str, *, strip_tones: bool = True, lowercase: bool = True) -> str:
    """Normalize a code for Rime."""
    code = code.strip()

    if strip_tones:
        code = strip_tone(code)

    # Rime input codes are easier to type if only ordinary ASCII letters remain.
    # After tone stripping, remove tone separators or other non-letter symbols.
    code = re.sub(r"[^A-Za-z]", "", code)

    if lowercase:
        code = code.lower()

    return code


def split_characters(characters: str) -> list[str]:
    """
    Split a homophone character cell into single-character Rime entries.

    Whitespace is ignored. This function treats each Unicode code point as one
    candidate, which is suitable for Chinese character homophone tables.
    """
    return [ch for ch in characters.strip() if not ch.isspace()]


def detect_columns(header: list[str]) -> tuple[int, int]:
    """Detect code and character columns from the CSV header."""
    normalized = [h.strip().lower() for h in header]

    code_candidates = {
        "syllable/combination",
        "syllable",
        "combination",
        "code",
        "romanization",
        "拼音",
        "讀音",
        "读音",
    }
    char_candidates = {
        "汉字",
        "漢字",
        "characters",
        "character",
        "chars",
    }

    code_idx = None
    char_idx = None

    for idx, name in enumerate(normalized):
        if name in code_candidates:
            code_idx = idx
        if name in char_candidates:
            char_idx = idx

    # Fallback for the current PhonConvert CSV format.
    if code_idx is None:
        code_idx = 0
    if char_idx is None:
        char_idx = 1

    return code_idx, char_idx


def read_homophone_csv(
    csv_path: Path,
    *,
    strip_tones: bool = True,
    lowercase: bool = True,
) -> list[tuple[str, str, int]]:
    """
    Read a homophone-character CSV and return Rime dictionary entries.

    Returns:
        A list of (character, code, weight) tuples.
    """
    entries: list[tuple[str, str, int]] = []
    seen: set[tuple[str, str]] = set()

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        code_idx, char_idx = detect_columns(header)

        # Higher earlier weights preserve the table order approximately.
        weight = 1_000_000

        for row in reader:
            if len(row) <= max(code_idx, char_idx):
                continue

            raw_code = row[code_idx].strip()
            chars = row[char_idx].strip()
            code = normalize_code(raw_code, strip_tones=strip_tones, lowercase=lowercase)

            if not code or not chars:
                continue

            for ch in split_characters(chars):
                key = (ch, code)
                if key in seen:
                    continue
                seen.add(key)
                entries.append((ch, code, weight))
                weight -= 1

    return entries


def yaml_quote(value: str) -> str:
    """Quote a string safely enough for simple YAML scalar values."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def make_schema_yaml(schema_id: str, schema_name: str, version: str) -> str:
    """Create a minimal Rime schema YAML."""
    return f"""# Rime schema
# encoding: utf-8
# Author information is intentionally left as placeholders.

schema:
  schema_id: {schema_id}
  name: {yaml_quote(schema_name)}
  version: {yaml_quote(version)}
  author:
    - "YOUR_NAME <YOUR_EMAIL>"

switches:
  - name: ascii_mode
    reset: 0
    states: [ 中文, ASCII ]

engine:
  processors:
    - ascii_composer
    - recognizer
    - key_binder
    - speller
    - punctuator
    - selector
    - navigator
    - express_editor
  segmentors:
    - ascii_segmentor
    - matcher
    - abc_segmentor
    - punct_segmentor
    - fallback_segmentor
  translators:
    - punct_translator
    - script_translator

speller:
  alphabet: "abcdefghijklmnopqrstuvwxyz"
  delimiter: " '"

translator:
  dictionary: {schema_id}
  enable_sentence: false
  enable_user_dict: true
  spelling_hints: 5

punctuator:
  import_preset: default

key_binder:
  import_preset: default

recognizer:
  import_preset: default
"""


def make_dict_yaml(schema_id: str, schema_name: str, version: str, entries: Iterable[tuple[str, str, int]]) -> str:
    """Create a Rime dictionary YAML."""
    lines = [
        "# Rime dictionary",
        "# encoding: utf-8",
        "# Author information is intentionally left as placeholders.",
        "",
        "---",
        f"name: {schema_id}",
        f"version: {yaml_quote(version)}",
        "sort: by_weight",
        "use_preset_vocabulary: false",
        "...",
        "",
    ]

    for char, code, weight in entries:
        lines.append(f"{char}\t{code}\t{weight}")

    return "\n".join(lines) + "\n"


def write_rime_files(
    csv_path: Path,
    output_dir: Path,
    *,
    schema_id: str,
    schema_name: str,
    version: str = "0.1.0",
    strip_tones: bool = True,
    lowercase: bool = True,
) -> tuple[Path, Path, int]:
    """Convert CSV and write Rime schema/dictionary files."""
    entries = read_homophone_csv(csv_path, strip_tones=strip_tones, lowercase=lowercase)

    output_dir.mkdir(parents=True, exist_ok=True)

    schema_path = output_dir / f"{schema_id}.schema.yaml"
    dict_path = output_dir / f"{schema_id}.dict.yaml"

    schema_path.write_text(make_schema_yaml(schema_id, schema_name, version), encoding="utf-8")
    dict_path.write_text(make_dict_yaml(schema_id, schema_name, version, entries), encoding="utf-8")

    return schema_path, dict_path, len(entries)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a PhonConvert homophone-character CSV table to a minimal tone-free Rime input method."
    )
    parser.add_argument("csv_path", type=Path, help="Input homophone-character CSV file.")
    parser.add_argument("-o", "--output-dir", type=Path, default=Path("rime_output"), help="Output directory.")
    parser.add_argument("--schema-id", default="romzj_input", help="Rime schema id. Use ASCII lowercase/underscore.")
    parser.add_argument("--schema-name", default="RomZJ Input", help="Display name of the Rime schema.")
    parser.add_argument("--version", default="0.1.0", help="Version string for generated YAML files.")
    parser.add_argument(
        "--keep-tone",
        action="store_true",
        help="Keep tone information in input codes. By default tones are removed.",
    )
    parser.add_argument(
        "--preserve-case",
        action="store_true",
        help="Preserve case in input codes. By default codes are lowercased.",
    )

    args = parser.parse_args()

    schema_path, dict_path, count = write_rime_files(
        args.csv_path,
        args.output_dir,
        schema_id=args.schema_id,
        schema_name=args.schema_name,
        version=args.version,
        strip_tones=not args.keep_tone,
        lowercase=not args.preserve_case,
    )

    print(f"Generated {count} dictionary entries.")
    print(f"Schema:     {schema_path}")
    print(f"Dictionary: {dict_path}")
    print("Tone information was removed from input codes." if not args.keep_tone else "Tone information was kept.")


if __name__ == "__main__":
    main()
