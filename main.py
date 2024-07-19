import time

from communicator.wire_serial import SerialConnection
from sensor.camera import ThreadedCamera

from task import TaskManager, ExecutionContext
from task.assignment_1 import CarRunOuterCircleNoUltrasound

from controller.car import Car

if __name__ == '__main__':
    serial_conn = SerialConnection()
    main_car = Car('main_car', serial_conn)
    camera = ThreadedCamera('laptop_camera')
    time.sleep(3)  # wait for camera to start

    context = ExecutionContext(camera=camera, main_car_controller=main_car, communication=serial_conn)
    task_manager = TaskManager(context)
    task_manager.add_task(CarRunOuterCircleNoUltrasound('test:FollowAndDetectTask'))
    task_manager.run()
