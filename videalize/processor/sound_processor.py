# -*- coding: utf-8 -*-

import numpy as np
import soundfile as sf
from videalize.logger import logger


class SoundProcessor:
    '''
    音量周りの処理
    '''

    def __init__(self, filename, blocksize=44100, method='HISTGRAM'):
        self.filename = filename
        self.blocksize = blocksize
        self.wav = self.load_volume_wav_per_blocks(blocksize)
        if method == 'MEDIAN':
            self.filtered_wav = self.cut_volume_by_median()
        else:
            self.filtered_wav = self.cut_volume_by_histgram()

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

    def cut_volume_by_histgram(self):
        '''
        ヒストグラムを二値化することで，境界を計算
        '''
        bins = 1000
        self.hist, self.bins = np.histogram(self.wav, bins)
        threshould = self.otsu_threshould()
        return [w if w >= threshould else 0 for w in self.wav]

    def otsu_threshould(self):
        '''
        大津の手法によるヒストグラムの二値化
        '''
        mean = np.mean(self.wav)
        max_idx = -1
        max_s = 0

        for t in range(1, len(self.bins)):
            left = self.hist[:t]
            right = self.hist[t:]

            var_l = np.var(left)
            mean_l = np.mean(left)
            n_l = np.sum(left)
            var_r = np.var(right)
            mean_r = np.mean(right)
            n_r = np.sum(right)

            inner_var = (n_l*var_l + n_r*var_r) / (n_l + n_r)
            between_var = (n_l * ((mean_l - mean)**2) + n_r * ((mean_r - mean)**2)) / (n_l + n_r)

            s = between_var / inner_var
            if s >= max_s:
                max_idx = t
                max_s = s

        return self.bins[max_idx]

    def make_cut_points(self):
        '''
        音量から切り出し点を計算
        '''
        cut_points = []
        start_idx = -1
        end_idx = -1

        for idx, w in enumerate(self.filtered_wav):
            if w == 0:
                if end_idx != -1:
                    point = {"start": start_idx * self.blocksize / 44100, "end": ((end_idx+1) * self.blocksize - 1) / 44100}
                    cut_points.append(point)
                    start_idx = -1
                    end_idx = -1
            else:
                if start_idx == -1:
                    start_idx = idx
                elif end_idx == -1 or end_idx == idx - 1:
                    end_idx = idx

        if start_idx != -1 and end_idx != -1:
            point = {"start": start_idx * self.blocksize / 44100, "end": ((end_idx+1) * self.blocksize - 1) / 44100}
            cut_points.append(point)

        logger.debug('extracted cut time using volume')
        return cut_points
