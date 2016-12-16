import speech_recognition as sr

from videalize import settings

class SoundRecognition:
    def __init__(self):
        self.username = settings.IBM_USERNAME
        self.password = settings.IBM_PASSWORD

    def recognize(self, filename):
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = r.record(source)
        return r.recognize_ibm(
            audio,
            username=self.username,
            password=self.password,
            language="ja-JP",
            show_all=True,
            timestamps=True
        )

if __name__ == '__main__':
    vr = SoundRecognition()
    print(vr.recognize('voice0.wav'))
