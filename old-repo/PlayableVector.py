#!/usr/bin/python
__author__ = "Chris Palmer, Brent Prox"
__license__ = "GPL"
__verson__ = "1.0.0"

import numpy as np

class PlayableVector():
	#members

	def setupHardcode(self, frequency, length, rate, amplitude):
		#create sin wave with specified parameters
		t = np.arange(length * rate)
		self.sinWave = float(amplitude) * np.sin(2*np.pi*t*(frequency/rate))
		pass

	def __init__(self):
		self.sinWave = []
		self.setupHardcode(frequency=440., length=1, rate=44100, amplitude=1)

	def getSample(self, timeIndex):
		# return the sample at a given time index for
		# the playable vector
		# - return none if passed 1 second (for now)
		pass

	# more helper functions will go here
	# trust me, they'll be the best

def main():
	pass
	pv = PlayableVector()
	print pv.sinWave


if __name__ == "__main__":
		main()
else:
		pass
