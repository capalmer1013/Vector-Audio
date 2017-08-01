"""
VAC Encoder Module
    This will initially be used to convert wav files to .vac
    down the road it will be used to convert arbitrary audio formats to .vac
"""
import wave
import sys


class File(object):
    def __init__(self):
        pass

    def write(self):
        pass

    pass


class Stream(object):
    pass


class State(object):
    FILETYPE = 0
    INIT_METADATA = 1
    METADATA = 2
    AUDIO_FRAMES = 3


def encode_file(filename):
    pass

if __name__ == "__main__":
    # at some point add a legitimate cli here
    encode_file(sys.argv[1])
    pass
