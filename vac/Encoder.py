"""
VAC Encoder Module
    This will initially be used to convert wav files to .vac
    down the road it will be used to convert arbitrary audio formats to .vac
"""
import logging
import wave
import sys


class File(object):
    def __init__(self, infilename=None):
        self.infile = infilename
        self.fsm = State()

    def encode(self, infilename=None):
        if not (self.infile and infilename):
            logging.error("No input file specified")
            raise Exception("No Input file")

        return self

    def writeOut(self, outfilename=None):
        return self


class Stream(object):
    pass


class State(object):
    FILETYPE = 0
    INIT_METADATA = 1
    METADATA = 2
    AUDIO_FRAMES = 3
    END = 4

    def __init__(self):
        self.currentState = self.FILETYPE
        self.bytesOut = ""

        # default metadata
        self.frame_size = 4096

        # state map
        self.states = {
            self.FILETYPE: self.file_type,
            self.INIT_METADATA: self.init_metadata,
            self.METADATA: self.metadata,
            self.AUDIO_FRAMES: self.audio_frame,
            self.END: self.end,
        }

    def setMetadata(self):
        # there will be some required fields here
        pass

    def listOfSignedInts(self, listOfInts):
        self.setMetadata()
        self.currentState = self.AUDIO_FRAMES
        for sample in listOfInts:
            self.execute_state(sample)

    def execute_state(self, next_input):
        self.states[self.currentState](next_input)
        pass

    def file_type(self, next_input):
        self.bytesOut += "VAC"

    def init_metadata(self, next_input):

        pass

    def metadata(self, next_input):
        pass

    def audio_frame(self, next_input):
        pass

    def end(self, next_input):
        pass

if __name__ == "__main__":
    # at some point add a legitimate cli here
    # proposed cli flags
    # -h print help screen and exit
    # -v print version
    # -V verbose
    # -d debug

    # this is a terrible cli
    if len(sys.argv) > 1:
        File(sys.argv[1]).encode().writeOut()

    else:
        logging.error("missing filename argument.")

    pass
