import cv2
import threading
import time
from config import Config
from logger_br import logger


class ProcessedFrame:
    frame = None

    def __init__(self, frame):
        self.frame = frame


class ThreadedCamera(object):
    """
    多线程摄像头类
    """

    def __init__(self, address, fps=1 / Config.get('camera.fps')):
        self.frame = None
        self.capture = cv2.VideoCapture(address)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 5)  # 设置最大缓冲区大小

        self.fps = fps  # 设置[检测]程序的采样速率,单位为秒, 默认为60帧每秒
        self.fps_ms = int(self.fps * 1000)

        self.detection_times = []  # 检测延迟

        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        while True:
            if self.capture.isOpened():
                (status, frame) = self.capture.read()
                if status:
                    self.frame = frame.copy()
            cv2.imshow('frame', self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(self.fps)

    def get_processed_data(self) -> ProcessedFrame:
        frame = self.frame
        if frame is None:
            return ProcessedFrame(None)

        return ProcessedFrame(frame=frame)

    def __del__(self):
        if hasattr(self, 'capture') and self.capture:
            self.capture.release()
        cv2.destroyAllWindows()
        # 关闭线程
        if hasattr(self, 'thread') and self.thread:
            self.thread.join()
        print("Camera closed successfully.")
