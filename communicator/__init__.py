from abc import ABC, abstractmethod


class Communicator(ABC):
    """
    通信父类，定义所有通信类应该遵循的接口。
    """

    @abstractmethod
    def send_data(self, data):
        """
        发送数据的方法，需要在子类中具体实现。
        :param data: 要发送的数据。
        """
        pass

    @abstractmethod
    def read_data(self):
        """
        读取数据的方法，需要在子类中具体实现。
        :return: 读取到的数据。
        """
        pass
