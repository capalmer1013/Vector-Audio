import audioop
import wave
import convertAudio
import playAudio


filename = input('input a file to convert or play: ')

if filename[-3:-1] == 'wav':
    waveFile = wave.open(filename, 'r')
    convertAudio.convertWaveFile(waveFile)

else:
    playAudio.playFile(filename)
