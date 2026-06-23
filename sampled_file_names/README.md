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
The Cantonese audio was first resampled to 24 kHz and saved as 16 bit PCM, then resampled again to 22.05 kHz and saved as 16 bit PCM.
The Mandarin audio was resampled to 22.05 kHz and saved as 16 bit PCM.
```
