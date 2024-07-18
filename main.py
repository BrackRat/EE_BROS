import time

from communicator.wire_serial import SerialConnection
from sensor.camera import ThreadedCamera

from task import TaskManager, ExecutionContext
from task.assignment_1 import FollowAndDetectTask

from controller.car import Car

if __name__ == '__main__':
    serial_conn = SerialConnection()
    car = Car('car_1', serial_conn)
    camera = ThreadedCamera('laptop_camera')
    time.sleep(5)  # wait for camera to start

    context = ExecutionContext(camera=camera, motor_pid=car.motor.pid, motor=car.motor)
    task_manager = TaskManager(context)
    task_manager.add_task(FollowAndDetectTask('test:FollowAndDetectTask'))
    task_manager.run()
