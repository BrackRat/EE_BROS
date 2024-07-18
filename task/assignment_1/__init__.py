import time

from controller.car import Motor
from task import Task
from logger_br import logger
from sensor.camera import ThreadedCamera
from task import ExecutionContext
from simple_pid import PID


class FollowAndDetectTask(Task):
    """
    在跟线的同时检测岔路口和终点。
    """

    def __init__(self, name, base_speed=30, max_speed=50):
        super().__init__(name)
        self.base_speed = base_speed
        self.max_speed = max_speed

    def execute(self, context: ExecutionContext):
        camera: ThreadedCamera = context['camera']
        pid: PID = context['motor_pid']
        motor: Motor = context['motor']

        if camera is None:
            logger.error("Camera not found.")
            return

        if pid is None:
            logger.error("PID not found.")
            return

        while True:
            processed_frame = camera.processed_frame
            if processed_frame is None:
                logger.error("Processed frame not found.")
                time.sleep(camera.fps)
                continue

            line_offset = processed_frame.line_offset
            logger.debug(f"Line offset: {line_offset}")

            if camera.processed_frame.turn_ready:
                logger.info("Turn ready.")
                motor.set_speed(0, 0)
                break

            # 通过PID控制小车
            pid_out = pid(line_offset)
            logger.debug(f"PID out: {pid_out}")

            speed_right = int(self.base_speed + pid_out)
            speed_left = int(self.base_speed - pid_out)
            if speed_right > self.max_speed:
                speed_right = self.max_speed
            if speed_left > self.max_speed:
                speed_left = self.max_speed

            logger.debug(f"Speed: left={speed_left}, right={speed_right}")
            motor.set_speed(speed_left, speed_right)
            time.sleep(camera.fps)

        # ToDo
        # 接下来，抵达岔路口时，进行中心线切换（左转直到新的中心线 然后直行）
