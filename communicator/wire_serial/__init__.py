import json
import time
import serial
from config import Config
from logger_br import logger
from communicator import Communicator


class SerialConnection(Communicator):
    def __init__(self, ):
        self.port = Config.get('serial.port')
        self.baudrate = Config.get('serial.baud_rate')
        self.serial = None
        self.open_connection()

    def open_connection(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate)
            self.serial.rts = False
            logger.info(f"Connected to {self.port} at {self.baudrate} baud.")
            # self.send_data({"message": "Hello, World!"})
        except Exception as e:
            logger.critical(f"Failed to open serial connection: {e}")

    def send_data(self, data: dict):
        if self.serial and self.serial.is_open:
            text = self.dict_to_json(data)
            try:
                self.serial.write(text.encode())
                logger.debug(f"Sent data: {text.strip()}")
                time.sleep(0.05)
            except Exception as e:
                logger.error(f"Failed to send data: {text.strip()} {e}")

    def read_data(self) -> dict | None:
        try:
            line = self.serial.readline()
            if line:
                return json.loads(line.decode('utf-8'))
            return None
        except Exception as e:
            logger.error(f"Failed to read data: {e}")
            return None

    def close_connection(self):
        if self.serial:
            self.serial.close()
            logger.info("Serial connection closed.")

    def dict_to_json(self, data: dict) -> str:
        return json.dumps(data) + "\n"

    def connection_lost(self, exc):
        logger.info("Connection closed.")
        if exc:
            logger.error(f"Connection lost due to {exc}")

    def pause_writing(self):
        logger.warning("Writing paused (buffer size exceeded).")

    def resume_writing(self):
        logger.info("Resumed writing.")

    def __del__(self):
        self.close_connection()
        logger.info("Serial connection closed.")
