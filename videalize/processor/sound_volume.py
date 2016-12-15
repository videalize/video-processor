import wave
import struct
import os

framesize = 20 #ms

def amplitude(data):
	return max(data)-min(data)

class Sound_Volume:
	#read file and calculate sound volume
	def __init__(self,filename):
		wr = wave.open(filename,"rb")
		self.volume = []
		frame = int(wr.getframerate()*framesize/1000)
		for i in range(int(wr.getnframes()/frame)):
			data = wr.readframes(frame)
			d = struct.unpack('%dh'%wr.getnchannels()*frame,data)
			if wr.getnchannels() == 2:
				d = d[::2]
			self.volume.append(amplitude(d))
		wr.close()

	#time(s)
	def getvolume(self,time):
		return self.volume[int(time*1000/framesize)]

	#time = [starttime(s),endtime(s)]
	def getvolumes(self,time):
		return self.volume[int(time[0]*1000/framesize):int(time[1]*1000/framesize)]

	def thresholding(self,noize = 0.1):
		noizevolume = max(self.volume)*noize
		voice = list(map(lambda x:x>noizevolume,self.volume))
		length = []
		start = -1
		if voice[0]:
			length.append(0)
		for i in range(len(self.volume)-1):
			if voice[i] != voice[i+1]:
				length.append(i-start)
				start = i
		return length

	#noize = noize_volume/voice_volume
	#mincutsize(s)
	#return voice point (not cutting point)
	def toarrays(self,noize = 0.01,mincutsize = 1):
		point = []
		length = self.thresholding(noize = noize)
		minsize = int(mincutsize*1000/framesize)
		collect = []
		yes = length[0]
		non = 0
		now = 0
		index = 0
		i = 1
		stack = 0
		while i < len(length)-1:
			if non+yes < minsize:
				non += length[i]
				yes += length[i+1]
				i += 2
			else:
				now = yes + non
				non = 0
				yes = length[i]
				stack = i
				i += 1
				break
		while i < len(length)-1:
			if non+yes < minsize:
				non += length[i]
				yes += length[i+1]
				i += 2
			else:
				if yes > non:
					collect.append(now)
					now = yes + non
					non = 0
					yes = length[i]
					stack = i
					i += 1
				else:
					now += length[stack] + length[stack+1]
					yes -= length[stack]
					non -= length[stack+1]
					stack += 2
		p = 0
		for x in range(0,len(collect)-1,2):
			p += collect[x]
			point.append({'start':p*framesize,'end':(p+collect[x+1])*framesize})
			p += collect[x+1]
		return point
