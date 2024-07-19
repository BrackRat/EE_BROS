from communicator import Communicator
from controller import Controller
from .motor import Motor
from .beeper import Beeper


class Car(Controller):
    def __init__(self, controller_id: str, communicator: Communicator):
        super().__init__(controller_id)
        self.motor = Motor("motor", communicator)
        self.beeper = Beeper("beeper", communicator)

    def beep(self, times: int):
        self.beeper.beep(times)

    def set_speed(self, left: int, right: int):
        self.motor.set_speed(left, right)

    def stop(self):
        self.motor.stop()
