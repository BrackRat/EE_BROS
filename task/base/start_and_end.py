from communicator import Communicator
from controller.car import Car
from task import Task, ExecutionContext
from logger_br import logger


class StartCommandTask(Task):
    def execute(self, context: ExecutionContext):
        communication: Communicator = context['communication_sub_car']
        communication.send_data({"cmd": "start"})
        logger.info("Start command sent to the other car.")


class StopCommandTask(Task):
    def execute(self, context: ExecutionContext):
        communication: Communicator = context['communication_sub_car']
        communication.send_data({"cmd": "stop"})
        logger.info("Start command sent to the other car.")


class StopTheCar(Task):
    def execute(self, context: ExecutionContext):
        car: Car = context['main_car_controller']
        car.stop()
        logger.info("Car stopped.")
