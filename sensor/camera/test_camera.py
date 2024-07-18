import cv2
from config import Config
from sensor.camera import ThreadedCamera

if __name__ == '__main__':
    camera = ThreadedCamera(address=Config.get('camera.address'))

    while True:
        result = camera.get_processed_data()
        if result.frame is None:
            continue
        cv2.imshow('frame', result.frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
