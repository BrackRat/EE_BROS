from abc import ABC, abstractmethod
from typing import Any, Dict
from logger_br import logger


class Sensor(ABC):
    """
    抽象传感器类，定义所有传感器共有的接口。
    """

    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id
        self.data: Dict[str, Any] = {}
        logger.info(f"Sensor {self.sensor_id} initialized.")

    @abstractmethod
    def update(self) -> bool:
        """
        更新传感器数据的方法。每个传感器需要根据其具体功能实现数据的采集和更新。
        """
        pass

    @abstractmethod
    def get_data(self) -> Any:
        """
        获取当前传感器数据的方法。返回一个字典，包含了所需的数据。
        """
        pass

    def __str__(self) -> str:
        return f"Sensor ID: {self.sensor_id}, Data: {self.get_data()}"
