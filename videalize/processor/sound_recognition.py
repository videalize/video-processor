import speech_recognition

from videalize import settings
from videalize.logger import logger

class SoundRecognition:
    def __init__(self, speech_cut_threshold=settings.SPEECH_CUT_THRESHOLD):
        self.speech_cut_threshold = speech_cut_threshold

    def process_file(self, filename):
        response = self.recognize(filename)
        return self.extract_times(response)

    def recognize(self, filename):
        r = speech_recognition.Recognizer()
        with speech_recognition.AudioFile(filename) as source:
            audio = r.record(source)
        logger.debug('receiving speech data from IBM API')
        result = r.recognize_ibm(
            audio,
            username=settings.IBM_USERNAME,
            password=settings.IBM_PASSWORD,
            language="ja-JP",
            show_all=True,
            timestamps=True
        )
        logger.debug('received speech data from IBM API')
        return result

    def extract_times(self, response):
        parts = []
        for result in filter(lambda x: x['final'], response['results']):
            alternative = max(result['alternatives'], key=lambda r: r['confidence'])
            start_time = min(alternative['timestamps'], key=lambda t: t[1])[1]
            end_time = max(alternative['timestamps'], key=lambda t: t[2])[2]
            if parts and start_time - parts[-1]['end'] <= self.speech_cut_threshold:
                parts[-1]['end'] = end_time
            else:
                parts.append({'start': start_time, 'end': end_time})
        return parts
