import time

from controller.car import Car
from sensor.camera import ThreadedCamera
from task import Task, ExecutionContext
from logger_br import logger


class FollowLineUntilTurnPoint(Task):
    """
    跟随线直到转弯点任务
    """

    def __init__(self, name: str, base_speed: int, max_speed_dela: int, clear_pid: bool):
        super().__init__(name)
        self.base_speed = base_speed
        self.max_speed_dela = max_speed_dela
        self.max_speed = base_speed + max_speed_dela
        self.min_speed = base_speed - max_speed_dela
        self.clear_pid = clear_pid

    def execute(self, context: ExecutionContext):
        camera: ThreadedCamera = context['camera']
        car: Car = context['main_car_controller']

        # change output limt to -delta -> delta
        car.motor.pid.output_limits = (-self.max_speed_dela, self.max_speed_dela)

        if self.clear_pid:
            car.motor.pid.reset()
            car.motor.pid.setpoint = 0

        if camera is None:
            logger.error("Camera not found.")
            return

        if car is None:
            logger.error("Car Controller not found.")
            return

        # 运行，直到到达转弯点
        while True:
            # 更新摄像头中的线
            processed_frame = camera.processed_frame
            if processed_frame is None:
                logger.error("Processed frame not found.")
                time.sleep(camera.fps)
                continue

            line_offset = processed_frame.line_offset
            logger.debug(f"Line offset: {line_offset}")

            # 检测是否到达转弯点
            if camera.processed_frame.turn_ready:
                logger.info("Turn ready.")
                return True

            # 通过PID控制小车
            pid_out = car.motor.pid(line_offset)
            logger.debug(f"PID out: {pid_out:.2f}")

            speed_right = int(self.base_speed + pid_out)
            speed_left = int(self.base_speed - pid_out)
            if speed_right > self.max_speed:
                speed_right = self.max_speed
            if speed_left > self.max_speed:
                speed_left = self.max_speed

            if speed_right < self.min_speed:
                speed_right = self.min_speed
            if speed_left < self.min_speed:
                speed_left = self.min_speed

            logger.debug(f"Speed: left={speed_left}, right={speed_right}")
            car.motor.set_speed(speed_left, speed_right)
            time.sleep(camera.fps)

            logger.debug("-" * 50)


class GoStraightTask(Task):
    def execute(self, context: ExecutionContext):
        raise NotImplementedError


class DriveToEndTask(Task):
    def execute(self, context: ExecutionContext):
        raise NotImplementedError
