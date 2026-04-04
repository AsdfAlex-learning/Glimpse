"""
键盘管理器
负责全局快捷键监听和配置
"""
from typing import Dict, Callable
from pynput import keyboard


class KeyboardManager:
    """键盘管理器 - 单例模式"""
    
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
        self._hotkeys = {}
        self._listener = None
        self._running = False
    
    def register_hotkey(self, hotkey: str, callback: Callable):
        """注册全局快捷键
        
        Args:
            hotkey: 快捷键字符串，如 "<ctrl>+<shift>+g"
            callback: 回调函数
        """
        self._hotkeys[hotkey] = callback
    
    def unregister_hotkey(self, hotkey: str):
        """注销全局快捷键
        
        Args:
            hotkey: 快捷键字符串
        """
        if hotkey in self._hotkeys:
            del self._hotkeys[hotkey]
    
    def start_listening(self):
        """开始监听全局快捷键"""
        if self._running:
            return
        
        def on_press(key):
            pass
        
        def on_release(key):
            pass
        
        # 创建热键监听器
        hotkey_dict = {hotkey: callback for hotkey, callback in self._hotkeys.items()}
        self._listener = keyboard.GlobalHotKeys(hotkey_dict)
        self._listener.start()
        self._running = True
    
    def stop_listening(self):
        """停止监听全局快捷键"""
        if self._running and self._listener:
            self._listener.stop()
            self._running = False
    
    def is_running(self) -> bool:
        """检查是否正在监听"""
        return self._running
    
    def get_hotkeys(self) -> Dict[str, Callable]:
        """获取所有注册的快捷键"""
        return self._hotkeys.copy()


keyboard_manager = KeyboardManager()