from abc import ABC
from typing import Any, Dict
from logger_br import logger


class Controller(ABC):
    """
    抽象传感器类，定义所有传感器共有的接口。
    """

    def __init__(self, controller_id: str):
        self.controller_id = controller_id
        self.data: Dict[str, Any] = {}
        logger.info(f"Sensor {self.controller_id} initialized.")

    def __str__(self) -> str:
        return f"Controller ID: {self.controller_id}"
