```text
Format:

Cantonese:
test  [wav_file_A].wav
train  [wav_file_B].wav
val  [wav_file_C].wav
...

Mandarin:
test  [wav_file_x].wav
train  [wav_file_y].wav
val  [wav_file_z].wav
...


There is a blank line between the Cantonese part and the Mandarin part.
The Cantonese audio was then processed for the S2R experiment in two stages: it was first resampled from 16 kHz and 32 bit floating point to 24 kHz and saved as 16 bit PCM, and then resampled to 22.05 kHz and saved again as 16 bit PCM.
The Mandarin audio was then directly resampled for the S2R experiment from 44.1 kHz and 16 bit PCM to 22.05 kHz and saved as 16 bit PCM.
```
