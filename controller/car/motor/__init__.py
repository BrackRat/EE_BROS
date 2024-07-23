from controller import Controller
from communicator import Communicator
from simple_pid import PID
from config import Config
from logger_br import logger


class Motor(Controller):
    kp = Config.get("motor.kp")
    ki = Config.get("motor.ki")
    kd = Config.get("motor.kd")
    pid = PID(kp, ki, kd)

    def __init__(self, controller_id: str, communicator: Communicator):
        super().__init__(controller_id)
        self.communicator = communicator
        logger.info(f"Motor PID: {self.pid}")

    def set_speed(self, left: int, right: int):
        self.communicator.send_data({"cmd": "set_speed", "left": left, "right": right})

    def stop(self):
        self.communicator.send_data({"cmd": "set_speed", "left": 0, "right": 0})
