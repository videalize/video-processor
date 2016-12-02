# -*- coding: utf-8 -*-

import numpy as np
import soundfile as sf
import json


class SoundProcessor:
    '''
    音量周りの処理
    '''

    def __init__(self, filename, blocksize=44100):
        self.filename = filename
        self.blocksize = blocksize
        self.wav = self.load_volume_wav_per_blocks(blocksize)
        self.filtered_wav = self.cut_volume_by_median()

    def load_wav(self):
        '''
        return (wav, fs)
        wav: wavデータ (numpy)
        fs: サンプリング周波数
        '''
        return sf.read(self.filename)

    def load_volume_wav_per_blocks(self, blocksize=44100):
        '''
        return wav
        wav: wavデータ (list)
        '''
        return [np.sqrt(np.mean(block**2)) for block in sf.blocks(self.filename, blocksize=blocksize)]

    def cut_volume_by_median(self):
        '''
        中央値未満の音量を0に変換
        '''
        med = np.median(self.wav)
        return [w if w >= med else 0 for w in self.wav]

    def make_cut_points_json(self):
        cut_points = []
        start_idx = -1
        end_idx = -1

        for idx, w in enumerate(self.filtered_wav):
            if w == 0:
                if end_idx != -1:
                    point = {"start": start_idx * self.blocksize, "end": (end_idx+1) * self.blocksize - 1}
                    cut_points.append(point)
                    start_idx = -1
                    end_idx = -1
            else:
                if start_idx == -1:
                    start_idx = idx
                elif end_idx == -1 or end_idx == idx - 1:
                    end_idx = idx

        if start_idx != -1 and end_idx != -1:
            point = {"start": start_idx * self.blocksize, "end": (end_idx+1) * self.blocksize - 1}
            cut_points.append(point)

        print(json.dumps({"cut_points": cut_points}))

        return json.dumps({"cut_points": cut_points})
