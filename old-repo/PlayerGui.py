#!/usr/bin/python
__author__ = "Chris Palmer, Brent Prox"
__license__ = "GPL"
__verson__ = "1.0.0"

import PlayableVector
import Nsound as ns
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

debug = True

class PlayerGui():
	def __init__(self):
		# initialize a gui to control the playing functions
		self.pv = PlayableVector.PlayableVector()
		self.currentPosition = 0
		self.SAMPLES_PER_SECOND = 44100
		self.buffer = ns.Buffer()
		self.debugSamples = []
		self.debugSetup()
	
	def play(self):
		# play from current position
		if not debug:
			while self.pv.getSample(self.currentPosition) is not None:
			
				# use nsound to play the sample
				# make sure player is waiting correct amount of time before plating next sample
				pass

		else:
			sampleNumber = self.debugGetSample(self.currentPosition)
			while sampleNumber is not None:
				print sampleNumber
				
				self.currentPosition += 1.0 / float(self.SAMPLES_PER_SECOND)
				sampleNumber = self.debugGetSample(self.currentPosition)
			print len(self.debugSamples)
			#sd.play(self.debugSamples, self.SAMPLES_PER_SECOND)

			#plt.plot(self.debugSamples)
			#plt.show()

			#f, df = 440.0, 44100.0
			#t = r_[0.0:1.0:1/df]
			#data = np.cos(2 * pi * f * t)
			#play(data)
			#data = np.random.uniform(-1, 1, 44100)

			data = self.debugSamples
			scaled = np.int16(data/np.max(np.abs(data)) * 32767)
			
			plt.plot(scaled)
			plt.show()
			
			sd.play(scaled, self.SAMPLES_PER_SECOND)
			#write('test1.wav', 44100, scaled)


	def pause(self):
		# stop the music playing and maintain current pos
		pass
		
	def stop(self):
		# stop the music and return to begining pos
		pass
		
	def changePosition(self, n):
		# given timeIndex change the players index to that
		pass
		
	def debugSetup(self):
		for i in range(self.SAMPLES_PER_SECOND*2):
			#self.debugSamples.append(0.0)
			self.debugSamples.append(np.sin(440*(float(i)/float(self.SAMPLES_PER_SECOND)))*1)


	def debugGetSample(self, n):
		try:
			n = int(n*self.SAMPLES_PER_SECOND)
			return self.debugSamples[n]
			
		except IndexError:
			return None
			
def main():
	pg = PlayerGui()
	
	exitMain = False
	
	# this will need to be multithreaded in the future
	while not exitMain:
		userInput = int(raw_input("1: play, 2: pause, 3: stop, 4: change starting pos, 0: exit: "))
		
		if userInput == 1:
			pg.play()
			
		elif userInput == 2:
			pg.pause()
			
		elif userInput == 3:
			pg.stop()
			
		elif userInput == 4:
			n = raw_input("enter new position: ")
			
			pg.changePosition(n)
			
		elif userInput == 0:
			exitMain = True
			
		else:
			print "invalid input"

if __name__ == "__main__":
	main()
