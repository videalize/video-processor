import cv2
import moviepy.editor as mpy
from .sound_processor import SoundProcessor

class Processor:
    def __init__(self, video_path):
        self.video_path = video_path
        self._video_length = None
        self._video_frame_count = None
        self.cv_capture = cv2.VideoCapture(video_path)
        self.video = mpy.VideoFileClip(video_path)
        self.output_video = None

        if not self.cv_capture.isOpened():
            raise IOError('could not open video {0}'.format(video_path))

    @property
    def video_length(self):
        if not self._video_length:
            self._video_length = int(self.video.duration * 1000)
        return self._video_length

    @property
    def output_video_length(self):
        return int(self.output_video.duration * 1000)

    def generate_thumbnail(self, output_file, relative_position=0.5):
        frame_time = self.video_length * relative_position
        self.seek_video(frame_time)
        success, frame = self.cv_capture.read()
        self.seek_video(0)
        if not success:
            raise RuntimeError('could not capture frame at {0}ms'.format(frame_time))
        cv2.imwrite(output_file, frame)

    def seek_video(self, position):
        self.cv_capture.set(cv2.CAP_PROP_POS_MSEC, position)

    def process_video(self, output_file):
        parts = self.extract_necessary_times()
        clips = [self.video.subclip(part['start'], part['end']) for part in parts]
        self.output_video = mpy.concatenate_videoclips(clips)
        self.output_video.write_videofile(output_file)

    def extract_necessary_times(self):
        audio_path = self.video_path.replace('mp4', 'wav')
        self.video.audio.write_audiofile(audio_path)
        # XXX: why 8820?
        sound_processor = SoundProcessor(audio_path, 8820)
        return sound_processor.make_cut_points()
