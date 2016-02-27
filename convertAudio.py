import
def convertWaveFile(waveFile):
    for i in range(waveFile.getnframes()):
        frame = waveFile.readframes(i)


