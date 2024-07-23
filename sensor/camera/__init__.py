import cv2
import threading
import time
from config import Config
from sensor import Sensor
from logger_br import logger

from .line_recoginze import get_line_position_from_img


class ProcessedFrame:
    frame = None
    line_offset = None
    turn_ready = None

    def __init__(self, frame, turn_ready, line_offset=None, ):
        self.frame = frame
        self.turn_ready = turn_ready
        self.line_offset = line_offset


class ThreadedCamera(Sensor):
    """
    多线程摄像头类
    """

    processed_frame = None

    def __init__(self, sensor_id: str, fps=1 / Config.get('camera.fps'), thresh=100, interactive_debug=False):
        super().__init__(sensor_id)
        self.frame = None
        self.capture = cv2.VideoCapture(Config.get('camera.address'))
        self.capture.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))  # 设置编码格式
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 5)  # 设置最大缓冲区大小
        # set capture size to 640x480
        self.capture.set(3, 640)
        self.capture.set(4, 480)

        self.fps = fps  # 设置[检测]程序的采样速率,单位为秒, 默认为60帧每秒
        self.fps_ms = int(self.fps * 1000)
        logger.debug(f"Camera: {sensor_id} address: {Config.get('camera.address')} | FPS: {1 / self.fps}")

        self.detection_times = []  # 检测延迟

        # 交互式调试
        self.thresh = thresh
        self.interactive_debug = interactive_debug

        self.thread = threading.Thread(target=self.update_thread, args=())
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"Camera: {sensor_id} initialized.")

    def update(self) -> bool:
        """
        由于是多线程摄像头，所以不需要更新
        :return: True
        """
        return True

    def update_thread(self):
        while True:
            if self.capture.isOpened():
                (status, frame) = self.capture.read()
                if status:
                    self.frame = frame.copy()

            # 处理
            line_position, img = get_line_position_from_img(self.frame,
                                                            thresh=self.thresh,
                                                            draw_img=True,
                                                            interactive=self.interactive_debug)

            self.processed_frame = ProcessedFrame(frame=img,
                                                  turn_ready=False,
                                                  line_offset=line_position)

            cv2.imshow('processed', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(self.fps)

    def get_data(self) -> ProcessedFrame:
        return self.processed_frame

    def __del__(self):
        if hasattr(self, 'capture') and self.capture:
            self.capture.release()
        cv2.destroyAllWindows()
        # 关闭线程
        if hasattr(self, 'thread') and self.thread:
            self.thread.join()
        print("Camera closed successfully.")
