# CantRomZJ1–Jyutping Python Utilities

This directory contains standalone Python utilities for converting between Jyutping and CantRomZJ1, parsing CantRomZJ1 syllables, and representing converted results as PyCantonese `Jyutping` objects.

The files are organized according to a one-public-function-per-file design:

- Each Python filename matches its public function name.
- Each file contains one top-level public function.
- No file imports another file from this directory.
- The mappings and helper logic required by a function are included in that function's own file.
- Individual files can therefore be copied into another project without copying the entire directory, provided that any required external dependency is also installed.

## Requirements

Python 3.10 or later is required because the files use modern type-hint syntax.

Install the external dependency with:

```bash
pip install -r requirements.txt
```

or:

```bash
pip install pycantonese
```

The following files require `pycantonese`:

- `jyutping_to_cantromzj1.py`
- `jyutping_syllable_to_cantromzj1.py`
- `parse_jyutping_to_cantromzj1_objects.py`
- `parse_cantromzj1.py`
- `parse_cantromzj1_syllable.py`

The following reverse-conversion files use only the Python standard library:

- `cantromzj1_to_jyutping.py`
- `cantromzj1_syllable_to_jyutping.py`

## Files and Functions

| File | Public function | Main purpose | Requires PyCantonese |
|---|---|---|---|
| `jyutping_to_cantromzj1.py` | `jyutping_to_cantromzj1()` | Converts one or more Jyutping syllables to CantRomZJ1 strings | Yes |
| `jyutping_syllable_to_cantromzj1.py` | `jyutping_syllable_to_cantromzj1()` | Converts exactly one Jyutping syllable to CantRomZJ1 | Yes |
| `parse_jyutping_to_cantromzj1_objects.py` | `parse_jyutping_to_cantromzj1_objects()` | Parses Jyutping and returns PyCantonese objects whose nucleus and tone fields use CantRomZJ1 notation | Yes |
| `cantromzj1_to_jyutping.py` | `cantromzj1_to_jyutping()` | Converts one or more CantRomZJ1 syllables to Jyutping strings | No |
| `cantromzj1_syllable_to_jyutping.py` | `cantromzj1_syllable_to_jyutping()` | Converts exactly one CantRomZJ1 syllable to Jyutping | No |
| `parse_cantromzj1.py` | `parse_cantromzj1()` | Parses one or more CantRomZJ1 syllables into PyCantonese-style objects | Yes |
| `parse_cantromzj1_syllable.py` | `parse_cantromzj1_syllable()` | Parses exactly one CantRomZJ1 syllable into a PyCantonese-style object | Yes |

## Quick Start

### Convert Jyutping to CantRomZJ1

```python
from jyutping_to_cantromzj1 import jyutping_to_cantromzj1

result = jyutping_to_cantromzj1(
    "hoeng1gong2",
    output_separator=" ",
    return_mode="string",
)

print(result)
# heong1A|55 gong2A|35
```

### Convert CantRomZJ1 to Jyutping

```python
from cantromzj1_to_jyutping import cantromzj1_to_jyutping

result = cantromzj1_to_jyutping(
    "heong1A|55 gong2A|35",
    output_separator=" ",
    return_mode="string",
)

print(result)
# hoeng1 gong2
```

The reverse-conversion functions apply the inverse mappings.

## Detailed Function Reference

### 1. `jyutping_to_cantromzj1()`

Import:

```python
from jyutping_to_cantromzj1 import jyutping_to_cantromzj1
```

Signature:

```python
jyutping_to_cantromzj1(
    jyutping: str,
    *,
    output_separator: str = "",
    return_mode: Literal["tuple", "string", "list"] = "tuple",
)
```

Purpose:

Converts a Jyutping string containing one or more syllables to CantRomZJ1. Concatenated input and input separated by ordinary spaces are both accepted.

Examples of accepted input:

```text
hoeng1gong2
hoeng1 gong2
```

Parameters:

- `jyutping`: A valid Jyutping string. Each syllable must include a tone number.
- `output_separator`: The string inserted between converted syllables in the joined output. The default is an empty string.
- `return_mode`: Controls the return type.
  - `"tuple"`: returns `(joined_string, syllable_list)`.
  - `"string"`: returns only the joined string.
  - `"list"`: returns only the list of converted syllables.

Examples:

```python
from jyutping_to_cantromzj1 import jyutping_to_cantromzj1

joined, syllables = jyutping_to_cantromzj1("hoeng1gong2")
print(joined)
# heong1A|55gong2A|35
print(syllables)
# ['heong1A|55', 'gong2A|35']
```

```python
result = jyutping_to_cantromzj1(
    "hoeng1 gong2",
    output_separator=" ",
    return_mode="string",
)
print(result)
# heong1A|55 gong2A|35
```

```python
result = jyutping_to_cantromzj1(
    "sik6",
    return_mode="list",
)
print(result)
# ['sik4B|2']
```

Behavior:

- Uses `pycantonese.parse_jyutping()` to parse the Jyutping input.
- Removes ordinary spaces before parsing.
- Applies the CantRomZJ1 nucleus mapping.
- Uses the checked-tone mapping when the coda is `p`, `t`, or `k`.
- Preserves the parsed onset and coda.

Errors:

- Invalid Jyutping input may raise an exception from PyCantonese.
- An unsupported tone and coda combination raises `ValueError`.
- An invalid `return_mode` raises `ValueError`.

### 2. `jyutping_syllable_to_cantromzj1()`

Import:

```python
from jyutping_syllable_to_cantromzj1 import jyutping_syllable_to_cantromzj1
```

Signature:

```python
jyutping_syllable_to_cantromzj1(jyutping_syllable: str) -> str
```

Purpose:

Converts exactly one Jyutping syllable to one CantRomZJ1 syllable.

Example:

```python
from jyutping_syllable_to_cantromzj1 import (
    jyutping_syllable_to_cantromzj1,
)

print(jyutping_syllable_to_cantromzj1("hoeng1"))
# heong1A|55

print(jyutping_syllable_to_cantromzj1("sik6"))
# sik4B|2
```

Behavior:

- Trims surrounding whitespace.
- Parses the input with PyCantonese.
- Requires the parser to return exactly one syllable.
- Applies the same nucleus and tone mappings as `jyutping_to_cantromzj1()`.

Errors:

- Zero parsed syllables or more than one parsed syllable raises `ValueError`.
- Invalid Jyutping may raise an exception from PyCantonese.
- An unsupported tone and coda combination raises `ValueError`.

Use this function when the application already processes input one syllable at a time.

### 3. `parse_jyutping_to_cantromzj1_objects()`

Import:

```python
from parse_jyutping_to_cantromzj1_objects import (
    parse_jyutping_to_cantromzj1_objects,
)
```

Signature:

```python
parse_jyutping_to_cantromzj1_objects(jyutping: str) -> list[Jyutping]
```

Purpose:

Parses Jyutping input and returns a list of `pycantonese.jyutping.Jyutping` objects in which:

- `onset` preserves the Jyutping onset;
- `nucleus` uses the CantRomZJ1 nucleus spelling;
- `coda` preserves the Jyutping coda;
- `tone` uses the CantRomZJ1 tone label.

Example:

```python
from parse_jyutping_to_cantromzj1_objects import (
    parse_jyutping_to_cantromzj1_objects,
)

items = parse_jyutping_to_cantromzj1_objects("hoeng1gong2")

for item in items:
    print(item)

# Jyutping(onset='h', nucleus='eo', coda='ng', tone='1A|55')
# Jyutping(onset='g', nucleus='o', coda='ng', tone='2A|35')
```

This function is useful when structured onset, nucleus, coda, and tone fields are needed instead of a formatted string.

Important note:

The returned objects use the PyCantonese `Jyutping` class as a structured container, but their `nucleus` and `tone` fields contain CantRomZJ1 notation. They should therefore not be treated as ordinary standard-Jyutping objects by other software without conversion.

### 4. `cantromzj1_to_jyutping()`

Import:

```python
from cantromzj1_to_jyutping import cantromzj1_to_jyutping
```

Signature:

```python
cantromzj1_to_jyutping(
    cantromzj1: str,
    *,
    output_separator: str = "",
    return_mode: Literal["tuple", "string", "list"] = "tuple",
)
```

Purpose:

Converts one or more CantRomZJ1 syllables to Jyutping. Both concatenated and space-separated CantRomZJ1 input are accepted.

Examples of accepted input:

```text
heong1A|55gong2A|35
heong1A|55 gong2A|35
```

Parameters:

- `cantromzj1`: A CantRomZJ1 string. Every syllable must end in a supported CantRomZJ1 tone label.
- `output_separator`: The string inserted between converted Jyutping syllables in the joined output.
- `return_mode`: Controls the return type.
  - `"tuple"`: returns `(joined_string, syllable_list)`.
  - `"string"`: returns only the joined string.
  - `"list"`: returns only the list of Jyutping syllables.

Examples:

```python
from cantromzj1_to_jyutping import cantromzj1_to_jyutping

joined, syllables = cantromzj1_to_jyutping(
    "heong1A|55gong2A|35"
)
print(joined)
# hoeng1gong2
print(syllables)
# ['hoeng1', 'gong2']
```

```python
result = cantromzj1_to_jyutping(
    "heong1A|55 gong2A|35",
    output_separator=" ",
    return_mode="string",
)
print(result)
# hoeng1 gong2
```

```python
result = cantromzj1_to_jyutping(
    "sik4B|2",
    return_mode="list",
)
print(result)
# ['sik6']
```

Behavior:

- If ordinary spaces are present, the input is split on whitespace.
- Otherwise, the function detects CantRomZJ1 tone labels and uses them as syllable boundaries.
- Each syllable is divided into onset, nucleus, coda, and tone.
- Syllabic `m` and `ng` are supported.
- The inverse nucleus and tone mappings are applied.

Errors:

- A missing or unsupported CantRomZJ1 tone label raises `ValueError`.
- An unsupported syllable body raises `ValueError`.
- Unparsed trailing content raises `ValueError`.
- An invalid `return_mode` raises `ValueError`.

### 5. `cantromzj1_syllable_to_jyutping()`

Import:

```python
from cantromzj1_syllable_to_jyutping import (
    cantromzj1_syllable_to_jyutping,
)
```

Signature:

```python
cantromzj1_syllable_to_jyutping(cantromzj1_syllable: str) -> str
```

Purpose:

Converts exactly one CantRomZJ1 syllable to one Jyutping syllable.

Example:

```python
from cantromzj1_syllable_to_jyutping import (
    cantromzj1_syllable_to_jyutping,
)

print(cantromzj1_syllable_to_jyutping("heong1A|55"))
# hoeng1

print(cantromzj1_syllable_to_jyutping("sik4B|2"))
# sik6
```

Behavior:

- Trims surrounding whitespace.
- Detects one supported CantRomZJ1 tone suffix.
- Splits the remaining body into onset, nucleus, and coda.
- Supports syllabic `m` and `ng`.
- Applies the inverse CantRomZJ1-to-Jyutping mappings.

Errors:

- A missing tone suffix raises `ValueError`.
- A missing segmental body raises `ValueError`.
- An unsupported syllable structure raises `ValueError`.

### 6. `parse_cantromzj1()`

Import:

```python
from parse_cantromzj1 import parse_cantromzj1
```

Signature:

```python
parse_cantromzj1(text: str) -> list[Jyutping]
```

Purpose:

Parses concatenated or space-separated CantRomZJ1 text into a list of `pycantonese.jyutping.Jyutping` objects. The object fields contain CantRomZJ1 components rather than converted Jyutping components.

Example:

```python
from parse_cantromzj1 import parse_cantromzj1

items = parse_cantromzj1(
    "heong1A|55 gong2A|35"
)

for item in items:
    print(item)

# Jyutping(onset='h', nucleus='eo', coda='ng', tone='1A|55')
# Jyutping(onset='g', nucleus='o', coda='ng', tone='2A|35')
```

Behavior:

- Accepts ordinary space-separated CantRomZJ1 syllables.
- Also accepts concatenated input by detecting tone labels as syllable boundaries.
- Splits each syllable into onset, nucleus, coda, and tone.
- Supports syllabic `m` and `ng`.
- Returns structured objects without converting the CantRomZJ1 nucleus or tone back to Jyutping.

Important note:

Although the returned class is named `Jyutping`, the `nucleus` and `tone` fields retain CantRomZJ1 notation. The class is being used as a convenient onset-nucleus-coda-tone container.

Errors:

- A missing tone label raises `ValueError`.
- Unparsed trailing content raises `ValueError`.
- An unsupported syllable body raises `ValueError`.

### 7. `parse_cantromzj1_syllable()`

Import:

```python
from parse_cantromzj1_syllable import parse_cantromzj1_syllable
```

Signature:

```python
parse_cantromzj1_syllable(syllable: str) -> Jyutping
```

Purpose:

Parses exactly one CantRomZJ1 syllable into one `pycantonese.jyutping.Jyutping` object whose fields preserve CantRomZJ1 notation.

Example:

```python
from parse_cantromzj1_syllable import parse_cantromzj1_syllable

item = parse_cantromzj1_syllable("heong1A|55")
print(item)
# Jyutping(onset='h', nucleus='eo', coda='ng', tone='1A|55')
```

Syllabic nasal example:

```python
item = parse_cantromzj1_syllable("m3B|22")
print(item)
# Jyutping(onset='', nucleus='m', coda='', tone='3B|22')
```

Behavior:

- Trims surrounding whitespace.
- Detects one supported tone suffix.
- Splits the body into onset, nucleus, and coda.
- Supports syllabic `m` and `ng`.
- Does not convert the parsed fields to Jyutping spelling.

Errors:

- A missing tone suffix raises `ValueError`.
- A missing segmental body raises `ValueError`.
- An unsupported syllable structure raises `ValueError`.

## Choosing the Appropriate Function

| Task | Recommended function |
|---|---|
| Convert a complete Jyutping string to a CantRomZJ1 string | `jyutping_to_cantromzj1()` |
| Convert one Jyutping syllable | `jyutping_syllable_to_cantromzj1()` |
| Convert Jyutping directly into structured CantRomZJ1 objects | `parse_jyutping_to_cantromzj1_objects()` |
| Convert a complete CantRomZJ1 string to Jyutping | `cantromzj1_to_jyutping()` |
| Convert one CantRomZJ1 syllable | `cantromzj1_syllable_to_jyutping()` |
| Parse CantRomZJ1 text without converting it to Jyutping | `parse_cantromzj1()` |
| Parse exactly one CantRomZJ1 syllable | `parse_cantromzj1_syllable()` |

## Standalone File Usage

Because each module is self-contained, one function can be copied independently into another project. For example, to use only reverse string conversion, copy:

```text
cantromzj1_to_jyutping.py
```

Then import it from the same directory:

```python
from cantromzj1_to_jyutping import cantromzj1_to_jyutping
```

No `__init__.py` or package installation is required for this direct module-level usage, as long as the directory containing the file is on Python's import path.

For a function that imports PyCantonese, install `pycantonese` in the same Python environment before running the file.
