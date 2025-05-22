# import os
# import yaml
# from easydict import EasyDict as edict


# class YamlParser(edict):
#     """
#     This is yaml parser based on EasyDict.
#     """

#     def __init__(self, cfg_dict=None, config_file=None):
#         if cfg_dict is None:
#             cfg_dict = {}

#         if config_file is not None:
#             assert(os.path.isfile(config_file))
#             with open(config_file, 'r') as fo:
#                 yaml_ = yaml.load(fo.read(), Loader=yaml.FullLoader)
#                 cfg_dict.update(yaml_)

#         super(YamlParser, self).__init__(cfg_dict)

#     def merge_from_file(self, config_file):
#         with open(config_file, 'r') as fo:
#             yaml_ = yaml.load(fo.read(), Loader=yaml.FullLoader)
#             self.update(yaml_)

#     def merge_from_dict(self, config_dict):
#         self.update(config_dict)


# def get_config(config_file=None):
#     return YamlParser(config_file=config_file)


# if __name__ == "__main__":
#     cfg = YamlParser(config_file="../configs/yolov3.yaml")
#     cfg.merge_from_file("../configs/deep_sort.yaml")

#     import ipdb
#     ipdb.set_trace()

import os
import yaml
from typing import Optional, Dict, Any

class YamlConfig:
    """
    YAML 配置解析器 (不依赖 EasyDict)
    支持嵌套字典的点式访问和文件合并
    """
    
    def __init__(self, cfg_dict: Optional[Dict[str, Any]] = None, config_file: Optional[str] = None):
        """
        初始化配置
        
        :param cfg_dict: 初始配置字典
        :param config_file: 配置文件路径
        """
        self._data = cfg_dict.copy() if cfg_dict else {}
        
        if config_file is not None:
            self.merge_from_file(config_file)
    
    def __getattr__(self, name: str) -> Any:
        """支持点式访问属性"""
        if name in self._data:
            # 如果是字典则包装成 YamlConfig 对象
            if isinstance(self._data[name], dict):
                return YamlConfig(self._data[name])
            return self._data[name]
        raise AttributeError(f"'YamlConfig' object has no attribute '{name}'")
    
    def __getitem__(self, key: str) -> Any:
        """支持字典式访问"""
        return self._data[key]
    
    def __contains__(self, key: str) -> bool:
        """支持 in 操作符"""
        return key in self._data
    
    def get(self, key: str, default: Any = None) -> Any:
        """安全获取配置项"""
        return self._data.get(key, default)
    
    def merge_from_file(self, config_file: str) -> None:
        """从 YAML 文件合并配置"""
        assert os.path.isfile(config_file), f"Config file {config_file} does not exist"
        
        with open(config_file, 'r') as f:
            yaml_config = yaml.safe_load(f) or {}
            self._merge_dict(self._data, yaml_config)
    
    def merge_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """从字典合并配置"""
        self._merge_dict(self._data, config_dict)
    
    def _merge_dict(self, base: Dict[str, Any], new: Dict[str, Any]) -> None:
        """递归合并字典"""
        for key, value in new.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                # 递归合并嵌套字典
                self._merge_dict(base[key], value)
            else:
                # 覆盖或新增键值
                base[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为普通字典"""
        return self._data
    
    def __repr__(self) -> str:
        return f"YamlConfig({self._data})"


def get_config(config_file: Optional[str] = None) -> YamlConfig:
    """获取配置对象的快捷函数"""
    return YamlConfig(config_file=config_file)


if __name__ == "__main__":
    # 使用示例
    cfg = YamlConfig(config_file="../configs/yolov3.yaml")
    cfg.merge_from_file("../configs/deep_sort.yaml")
    
    # 访问配置项
    print(cfg.model)  # 点式访问
    print(cfg["training"]["batch_size"])  # 字典式访问
    
    # 合并字典
    cfg.merge_from_dict({"new_key": "value"})