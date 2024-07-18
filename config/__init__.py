import json
import os

class Config:
    _config = None

    @classmethod
    def _load_config(cls):
        # 这里确保路径回退到项目根目录 EE_BROS，不超过这个目录
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(root_path, 'config.json')
        with open(config_path, 'r') as config_file:
            cls._config = json.load(config_file)

    @classmethod
    def get(cls, key):
        if cls._config is None:
            cls._load_config()
        return cls._config.get(key, None)
