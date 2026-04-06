"""
键盘管理器
负责全局快捷键监听和配置
"""
from typing import Dict, Callable, Optional
from pynput import keyboard
from threading import Lock


class KeyboardManager:
    """键盘管理器 - 单例模式"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._hotkeys: Dict[str, Callable] = {}
        self._listener: Optional[keyboard.GlobalHotKeys] = None
        self._running = False
        self._listener_lock = Lock()
    
    def register_hotkey(self, hotkey: str, callback: Callable):
        """注册全局快捷键
        
        Args:
            hotkey: 快捷键字符串，如 "<ctrl>+<shift>+g"
            callback: 回调函数
        """
        with self._lock:
            self._hotkeys[hotkey] = callback
    
    def unregister_hotkey(self, hotkey: str):
        """注销全局快捷键
        
        Args:
            hotkey: 快捷键字符串
        """
        with self._lock:
            if hotkey in self._hotkeys:
                del self._hotkeys[hotkey]
    
    def clear_hotkeys(self):
        """清空所有已注册的快捷键"""
        with self._lock:
            self._hotkeys.clear()
    
    def _create_listener_locked(self):
        """在持有_lock的情况下创建热键监听器（内部方法）"""
        hotkey_dict = {hotkey: callback for hotkey, callback in self._hotkeys.items()}
        if hotkey_dict:
            self._listener = keyboard.GlobalHotKeys(hotkey_dict)
            return True
        return False
    
    def start_listening(self):
        """开始监听全局快捷键"""
        with self._listener_lock:
            if self._running:
                return
            with self._lock:
                if self._create_listener_locked():
                    self._listener.start()
                    self._running = True
    
    def stop_listening(self):
        """停止监听全局快捷键"""
        with self._listener_lock:
            if self._running and self._listener:
                self._listener.stop()
                self._running = False
                self._listener = None
    
    def restart_listening(self):
        """重启键盘监听（用于热更新快捷键）

        锁顺序：统一先 _listener_lock，再 _lock
        异常处理：创建失败时保持停止状态，不半初始化
        """
        with self._listener_lock:
            old_listener = self._listener
            old_running = self._running

            self._listener = None
            self._running = False

            try:
                if old_running and old_listener:
                    old_listener.stop()

                with self._lock:
                    if self._hotkeys:
                        if self._create_listener_locked():
                            self._listener.start()
                            self._running = True
            except Exception:
                self._listener = None
                self._running = False
                raise

    def is_running(self) -> bool:
        """检查是否正在监听"""
        return self._running

    def get_hotkeys(self) -> Dict[str, Callable]:
        """获取所有注册的快捷键"""
        with self._lock:
            return self._hotkeys.copy()

    def reload_hotkeys(self, hotkeys: Dict[str, Callable]) -> bool:
        """重新加载快捷键配置（原子操作）

        Args:
            hotkeys: 新的快捷键字典

        Returns:
            是否重载成功
        """
        old_hotkeys = None
        old_listener = None
        old_running = False

        try:
            with self._listener_lock:
                with self._lock:
                    old_hotkeys = self._hotkeys.copy()
                    old_listener = self._listener
                    old_running = self._running

                    if old_running and old_listener:
                        old_listener.stop()

                    self._hotkeys = hotkeys.copy()
                    self._listener = None
                    self._running = False

                    if self._hotkeys:
                        if self._create_listener_locked():
                            self._listener.start()
                            self._running = True

                    return True
        except Exception:
            with self._listener_lock:
                with self._lock:
                    if old_listener and old_running:
                        try:
                            old_listener.start()
                            self._listener = old_listener
                            self._running = old_running
                            self._hotkeys = old_hotkeys
                        except Exception:
                            self._listener = None
                            self._running = False
                    else:
                        self._hotkeys = old_hotkeys
            return False


keyboard_manager = KeyboardManager()