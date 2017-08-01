# Vector-Audio
Audio files represented as continuous formulas instead of discrete samples

Basing a lot of the design off of (libFLAC)[https://xiph.org/flac/api/index.html]

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