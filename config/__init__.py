import json
import os


class Config:
    _config = None

    @classmethod
    def _load_config(cls):
        # 这里确保路径回退到项目根目录
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(root_path, 'config.json')
        with open(config_path, 'r', encoding='utf-8') as config_file:
            cls._config = json.load(config_file)

    @classmethod
    def get(cls, key):
        if cls._config is None:
            cls._load_config()
        key = key + ".value"  # 为了适配 F-BROS
        keys = key.split('.')
        value = cls._config
        for k in keys:
            value = value.get(k)
            if value is None:
                break
        return value
