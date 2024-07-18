from controller import Controller
from communicator import Communicator


class Beeper(Controller):
    def __init__(self, controller_id: str, communicator: Communicator):
        super().__init__(controller_id)
        self.communicator = communicator

    def beep(self, times: int):
        self.communicator.send_data({"cmd": "beep", "times": times})
