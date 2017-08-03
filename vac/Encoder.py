"""
VAC Encoder Module
    This will initially be used to convert wav files to .vac
    down the road it will be used to convert arbitrary audio formats to .vac
"""
import logging
import wave
import sys
import struct
import operator


class File(object):
    def __init__(self, infilename=None):
        self.infile = infilename
        self.fsm = State()

    def encode(self, infilename=None):
        if infilename: 
            self.infile = infilename

        if not self.infile:
            logging.error("No input file specified")
            raise Exception("No Input file")

        left, right = getSignedIntsFromWav(self.infile)
        listOfSamples = [x for t in zip(left, right) for x in t]
        self.fsm.listOfSignedInts(listOfSamples)

        return self

    def writeOut(self, outfilename=None):
        if not outfilename:
            raise Exception("no filename given")

        with open(outfilename, 'w') as f:
            f.write(self.fsm.bytesOut)

        return self


class Stream(object):
    """
    this currently isn't used for anything
    """
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

        # work in progress properties
        self.listOfSamples = []

        # default metadata
        self.nchannels = 2      # number of channels
        self.sampleSize = 2     # bytes per sample
        self.frame_size = 4096  # samples per frame
        self.sample_freq = 44100 # samplerate

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
        """
        given a list of samples as signed ints
        generate a binary file to output
        """
        self.setMetadata()
        self.file_type(0)
        self.init_metadata(0)
        self.currentState = self.AUDIO_FRAMES
        for sample in listOfInts:
            self.execute_state(sample)

        self.end(0)

    def execute_state(self, next_input):
        self.states[self.currentState](next_input)

    # States begin here ----------------------------------------------------------

    def file_type(self, next_input):
        self.bytesOut += "VAClerp"
        return self.INIT_METADATA

    def init_metadata(self, next_input):
        # add important metadata
        self.bytesOut += "ch:" + str(self.nchannels) +";"
        self.bytesOut += "byteDepth:" + str(self.sampleSize) + ";"
        self.bytesOut += "frameSize:" + str(self.frame_size) + ";"
        self.bytesOut += "sampleFreq:" + str(self.sample_freq) +";"
        return self.METADATA

    def metadata(self, next_input):
        # add optional metadata
        self.bytesOut += "END_META"
        return self.AUDIO_FRAMES

    def audio_frame(self, next_input):
        if len(self.listOfSamples) < self.frame_size:
            self.listOfSamples.append(next_input)
            return

        self.bytesOut += self.find_best_fit(self.listOfSamples)
        self.listOfSamples = []

    def end(self, next_input):
        self.bytesOut += self.find_best_fit(self.listOfSamples)
        self.listOfSamples = []

    # states end here ----------------------------------------------------------

    def find_best_fit(self, listOfSamples):
        """
        New approach:
            find and store points of interest
            - x intersect
            - nodemin
            - nodemax
            - inflectionpoints
        format:
            for POIs (might not need to be in order. since the whole frame is computed at the same time)
            - 2 bytes unsigned int x (sample index) this makes the max framesize 65k
            - 2 bytes signed int y (sample amplitude)
        """
        def findPOIs(listOfSamples):
            # listOfSamples: int -> [(x: int, y: int)]
            lastSample = None
            POIlist = []
            x = -1

            # get the x intercepts -----------------------------------------
            for sample in listOfSamples:
                x += 1
                if lastSample is None:
                    lastSample = sample
                    continue

                if lastSample <= 0 and sample > 0:
                    POIlist.append((x, lastSample))
            
            # get the node min and max --------------------------------------
            minmaxList = []
            nodesList = []
            tmp = []
            for each in POIlist:
                if len(tmp) < 2:
                    tmp.append(each[0])
                
                tmp.append(each[0])

                if len(tmp) > 2:
                    tmp.pop(0)
                
                nodesList.append(tuple(tmp))

            for poi in nodesList:
                try:
                    index, value = max(enumerate(listOfSamples[poi[0]:poi[1]]), key=operator.itemgetter(1))
                except ValueError:
                    # max value of empty list
                    index = len(listOfSamples)-1
                    value = listOfSamples[index]

                except Exception as e:
                    print "listOfSamples:", listOfSamples
                    print "poi", poi
                    raise e

                minmaxList.append((index+poi[0], value))

                try:
                    index, value = min(enumerate(listOfSamples[poi[0]:poi[1]]), key=operator.itemgetter(1))
                except ValueError:
                    # min value of empty list
                    index = len(listOfSamples)-1
                    value = listOfSamples[index]

                except Exception as e:
                    print "listOfSamples:", listOfSamples
                    print "poi", poi
                    raise e

                minmaxList.append((index+poi[0], value))

            POIlist.extend(minmaxList)

            # todo figure out how to find inflection points
            return POIlist


        
        poiList = findPOIs(listOfSamples)
        return "FRAME" + ''.join([struct.pack('h', x[0]) + struct.pack('h', x[1]) for x in poiList])


def writeWavFromSignedInts(outFilename, tupleOfInts):
    """
    if the len of the tuple is 1 then mono
    if 2 then stereo
    """
    outfile = wave.open(outFilename, "w")
    outfile.setnchannels(len(tupleOfInts))
    outfile.setsampwidth(2)  # lazy
    outfile.setframerate(44100)
    if len(tupleOfInts) == 1:
        # mono
        pass
    elif len(tupleOfInts) == 2:
        # interleaved stereo
        for i in range(len(tupleOfInts[0])):
            frame = struct.pack('h', tupleOfInts[0][i]) + struct.pack('h', tupleOfInts[1][i])
            outfile.writeframes(frame)
    else:
        raise Exception("more than 2 channels not supported")


def getSignedIntsFromWav(infileName):
    """
    given: a .wav filename
    return: a tuple of lists of ints
    """
    tmp = wave.open(infileName)
    nChannels = tmp.getnchannels()
    sampleWidth = tmp.getsampwidth()
    channels = None

    if nChannels == 1:
        channels = ([],)
        for _ in range(tmp.getnframes()):
            currentFrame = tmp.readframes(1)
            channels[0].append(struct.unpack('h', currentFrame[:sampleWidth])[0])

    elif nChannels == 2:
        # i[0] == left, i[1] == right
        channels = ([], [])
        for _ in range(tmp.getnframes()):
            currentFrame = tmp.readframes(1)
            channels[0].append(struct.unpack('h', currentFrame[:sampleWidth])[0])
            channels[1].append(struct.unpack('h', currentFrame[sampleWidth:])[0])

    else:
        raise Exception("More than 2 channels not supported")

    return channels

if __name__ == "__main__":
    # at some point add a legitimate cli here
    # proposed cli flags
    # -h print help screen and exit
    # -v print version
    # -V verbose
    # -d debug

    # this is a terrible cli
    if len(sys.argv) > 1:
        File(sys.argv[1]).encode().writeOut("testOut.vac")

    else:
        logging.error("missing filename argument.")
