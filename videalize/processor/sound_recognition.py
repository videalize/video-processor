import speech_recognition as sr

from videalize import settings

class SoundRecognition:
    def __init__(self, speech_cut_threshold=settings.SPEECH_CUT_THRESHOLD):
        self.speech_cut_threshold = speech_cut_threshold

    def process_file(self, filename):
        response = self.recognize(filename)
        return self.extract_times(response)

    def recognize(self, filename):
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = r.record(source)
        return r.recognize_ibm(
            audio,
            username=settings.IBM_USERNAME,
            password=settings.IBM_PASSWORD,
            language="ja-JP",
            show_all=True,
            timestamps=True
        )

    def extract_times(self, response):
        parts = []
        for result in filter(lambda x: x['final'], response['results']):
            alternative = max(result['alternatives'], key=lambda r: r['confidence'])
            start_time = min(alternative['timestamps'], key=lambda t: t[1])[1]
            end_time = min(alternative['timestamps'], key=lambda t: t[2])[2]
            if parts and start_time - parts[-1]['end'] <= self.speech_cut_threshold:
                parts[-1]['end'] = end_time
            else:
                parts.append({'start': start_time, 'end': end_time})
        return parts
