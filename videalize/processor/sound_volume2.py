# -*- coding: utf-8 -*-

import sys

import numpy as np
import scipy.fftpack as fft
import matplotlib.pyplot as plt
from argparse import ArgumentParser

import soundfile as sf
import json

from SoundProcessor import SoundProcessor
from processor import Processor

if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) <= 2:
        print("arg err")
        exit(1)

    sound_processor = SoundProcessor(sys.argv[1], int(sys.argv[2]))
    # sound_processor.cut_volume_by_median()
    # sound_processor.cut_volume_by_histgram()
    #
    # print(sound_processor.otsu_threshould())

    # plt.plot(range(len(sound_processor.hist)), sound_processor.hist)
    # plt.hist(sound_processor.hist, 1000)
    # plt.show()
    # print(sound_processor.make_cut_points_json)
    cp = sound_processor.make_cut_points()

    #processor = Processor('../../videos/lecture_sample.mp4')
    #processor.process_video('../../videos/test.mp4')



    # 横軸：時間，縦軸：音量のグラフを出力
    # plt.plot(np.array(range(len(sound_processor.filtered_wav))), sound_processor.filtered_wav)
    # plt.show()

    # argumentParser = ArgumentParser()
    # argumentParser.add_argument('-f', '--filename', type=str, required=True)

    # wavファイル読み込み
    # filename = sys.argv[1]
    # wav, fs = sf.read(filename)
    # wav = [w ** 2 for w in wav]

    # 音量レベルの計算
    # blocksize = int(sys.argv[2])
    # wav = [np.sqrt(np.mean(block**2)) for block in sf.blocks(filename, blocksize=blocksize)]
    #
    # print(len(wav))
    # print(type(wav))
    # med = np.median(wav)
    # print(med)
    # ave = np.average(wav)
    # print(ave)
    #
    # filtered_wav = [w if w >= med else 0 for w in wav]
    # print(filtered_wav.count(0))
    #
    # arr = []
    # start_idx = -1
    # end_idx = -1
    # for idx, w in enumerate(filtered_wav):
    #     if w == 0:
    #         if end_idx != -1:
    #             point = {"start": start_idx * blocksize, "end": (end_idx+1) * blocksize - 1}
    #             arr.append(point)
    #             start_idx = -1
    #             end_idx = -1
    #     else:
    #         if start_idx == -1:
    #             start_idx = idx
    #         elif end_idx == -1 or end_idx == idx - 1:
    #             end_idx = idx
    #
    # if start_idx != -1 and end_idx != -1:
    #     point = {"start": start_idx * blocksize, "end": (end_idx+1) * blocksize - 1}
    #     arr.append(point)
    #
    # print(json.dumps({"cut_point": arr}))
    # # ステレオ2chをLchとRchに分割
    # # wav_l = wav[:, 0]
    # # print(wav_l[374319])
    # # wav_r = wav[:, 1]
    #
    # # 入力をモノラル化
    # # xs = (0.5 * wav_l) + (0.5 * wav_r)
    # # print(xs.shape)
    #
