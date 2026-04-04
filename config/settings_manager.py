"""
设置管理器
负责配置的读写和管理
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional

from config.path_manager import path_manager


class SettingsManager:
    """设置管理器 - 单例模式"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._settings_file = path_manager.config_dir / "settings.json"
        self._settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """加载设置文件"""
        if not self._settings_file.exists():
            return self._get_default_settings()
        
        try:
            with open(self._settings_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._get_default_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """获取默认设置"""
        default_settings = {
            "hotkeys": {
                "screenshot": "<ctrl>+<shift>+g",
                "search": "<ctrl>+f",
                "clear": "<escape>"
            },
            "screenshot": {
                "debounce_interval": 5.0,
                "cluster_threshold": 2.0,
                "max_captures_per_window": 10
            },
            "ai": {
                "api_key": "",
                "model": "gpt-4o-mini",
                "timeout": 30
            },
            "ocr": {
                "engine": "rapidocr",
                "language": "ch"
            },
            "database": {
                "sqlite_timeout": 30,
                "chroma_collection": "memories"
            },
            "ui": {
                "theme": "light",
                "auto_hide": false,
                "start_minimized": false
            }
        }
        
        # 保存默认设置
        self._save_settings(default_settings)
        return default_settings
    
    def _save_settings(self, settings: Dict[str, Any]):
        """保存设置到文件"""
        try:
            with open(self._settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except IOError:
            pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取设置值
        
        Args:
            key: 设置键，支持点号分隔的路径，如 "hotkeys.screenshot"
            default: 默认值
            
        Returns:
            设置值或默认值
        """
        keys = key.split('.')
        value = self._settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """设置值
        
        Args:
            key: 设置键，支持点号分隔的路径
            value: 设置值
            
        Returns:
            是否设置成功
        """
        keys = key.split('.')
        settings = self._settings
        
        # 导航到目标位置
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        # 设置值
        settings[keys[-1]] = value
        
        # 保存设置
        self._save_settings(self._settings)
        return True
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有设置"""
        return self._settings.copy()
    
    def update(self, settings: Dict[str, Any]) -> bool:
        """更新多个设置
        
        Args:
            settings: 要更新的设置
            
        Returns:
            是否更新成功
        """
        try:
            self._settings.update(settings)
            self._save_settings(self._settings)
            return True
        except Exception:
            return False
    
    def reset(self):
        """重置为默认设置"""
        self._settings = self._get_default_settings()


settings_manager = SettingsManager()