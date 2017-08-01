import numpy


def str_to_int(s):
    i = int(s, 16)
    if i >= 2**7:
        i -= 2**8
    return i


def int_to_str(i):
    return '%06x' % ((i+2**24) % 2**24)


def convertWaveFile(waveFile, filename):
    numberOfFrames = waveFile.getnframes()
    numberOfChannels = waveFile.getnchannels()
    sampleRate = waveFile.getframerate()
    bitDepth = waveFile.getsampwidth() * 8
    # for i in range(0, numberOfFrames):
    #     byteString = waveFile.readframes(i)
    #     byteArray = [elem.encode("hex") for elem in byteString]
    #     print byteArray

    byteString = waveFile.readframes(numberOfFrames)
    # byteArray = [elem.encode("hex") for elem in byteString]
    for elem in byteString:
        print elem.encode("hex")
        print float(str_to_int(elem.encode("hex")))
    # print byteArray
    print waveFile.getnframes()
    print waveFile.getsampwidth()

