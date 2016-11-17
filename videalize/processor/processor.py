import cv2
import av

class Processor:
    def __init__(self, video_path):
        self._video_length = None
        self._video_frame_count = None
        self.cv_capture = cv2.VideoCapture(video_path)
        self.video_container = av.open(video_path)

        if not self.cv_capture.isOpened():
            raise IOError('could not open video {0}'.format(video_path))

    @property
    def video_length(self):
        if not self._video_length:
            self._video_length = self.video_container.duration / 1000
        return self._video_length

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
