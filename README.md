# Vector-Audio
Audio files represented as continuous formulas instead of discrete samples

Basing a lot of the design off of [libFLAC](https://xiph.org/flac/api/index.html)

*VAC* - Vector Audio Codec

## Sections:
- **Decoder:**
    - Will be used to convert .vac files to other formats first .wav

- **Encoder:**
    - Will be used to convert other file formats to .vac

- **MetaData:**
    - representation of metadata to encode or decode from .vac files

- **Player:**
    - official player for .vac files
    
## Format:
- 3 byte string "VAC"
- INITIAL metadata block
- 0 or more metadata blocks
- 1 or more audio frames

## Notes:
look into pyaudio (requires port audio)
[PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
possible algorithm to try for finding best fit function
- start with lowest fundamental for frame (1 cycle or 1/2 cycle)
- hill climb to offset with lowest error
- adjust amplitude
- proceed to next harmonic (or some other method of choosing pitches) (something with avg frequency, start with lowest harmonic)

**Things that might be important for estimating functions**
- x intersects
- inflection points
- node max/min amplitudes

A very naive approach would be to have a table of these points of interest and lerping between them.
This would definitely be lossy.

These could be different variations with different filetype names like VAClerp

## Version:
**0.1.0**
