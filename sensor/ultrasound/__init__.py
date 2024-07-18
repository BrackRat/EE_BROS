from sensor import Sensor
from communicator import Communicator


class Ultrasound(Sensor):
    def __init__(self, sensor_id: str, communicator: Communicator, max_try_times: int = 1000):
        super().__init__(sensor_id)
        self.distance = None
        self.communicator = communicator
        self.max_try_times = max_try_times

    def update(self) -> bool:
        self.communicator.send_data({"cmd": "get_distance"})
        try_times = 0
        while self.max_try_times > try_times:
            data = self.communicator.read_data()
            if data is None:
                continue
            if data.get("cmd") == "get_distance":
                self.distance = data.get("distance")
                break
            try_times += 1
        if self.distance is None:
            return False
        return True

    def get_data(self):
        return self.data
