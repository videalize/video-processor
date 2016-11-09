import wave
import struct
import os

def amplitude(data):
	return max(data)-min(data)

if __name__ == '__main__':
	wr = wave.open("voice.wav","rb")
	i = 10*wr.getframerate()
	j = 0
	powers = []
	while i < wr.getnframes():
		data = wr.readframes(10*wr.getframerate())
		d = struct.unpack('%dh'%10*wr.getnchannels()*wr.getframerate(),data)
		d = d[::2]
		powers.append((j,amplitude(d)))
		i += 10*wr.getframerate()
		j += 10
	vest = sorted(powers,key=lambda student: student[1])[-6:]
	vest = sorted(vest,key=lambda student: student[0])
	for k in range(6):
		print('ffmpeg -i "線形代数I (2013) (2) 平面ベクトルのスカラー倍，和，線形結合 (Linear Algebra I (2013), Lecture 2)-pRvkrKXxXN0.mp4" -vcodec copy -acodec copy -t 10 -ss %d output/%d.mp4'%(vest[k][0],k))
		os.system('ffmpeg -i "線形代数I (2013) (2) 平面ベクトルのスカラー倍，和，線形結合 (Linear Algebra I (2013), Lecture 2)-pRvkrKXxXN0.mp4" -vcodec copy -acodec copy -t 10 -ss %d output/%d.mp4'%(vest[k][0],k))
	wr.close()
