from controller import Controller
from communicator import Communicator
from simple_pid import PID


class Motor(Controller):
    pid = PID(0.013, 0, 0.02, )

    def __init__(self, controller_id: str, communicator: Communicator):
        super().__init__(controller_id)
        self.communicator = communicator

    def set_speed(self, left: int, right: int):
        self.communicator.send_data({"cmd": "set_speed", "left": left, "right": right})

    def stop(self):
        self.communicator.send_data({"cmd": "set_speed", "left": 0, "right": 0})
