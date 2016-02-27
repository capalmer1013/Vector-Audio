import audioop
import wave
import convertAudio
import playAudio


filename = raw_input('input a file to convert or play: ')

print filename
if filename[-3:len(filename)] == 'wav':
    waveFile = wave.open(filename, 'r')
    convertAudio.convertWaveFile(waveFile, filename)

else:
    playAudio.playFile(filename)
