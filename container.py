"""
DI Container - 依赖注入容器
统一管理所有单例服务实例的创建与访问
"""
import threading
from typing import Optional, Callable, Any, List


class DIContainer:
    """依赖注入容器 - 线程安全单例"""

    _instance: Optional["DIContainer"] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        with DIContainer._lock:
            if self._initialized:
                return
            self._initialized = True
            self._services: dict = {}
            self._factories: dict = {}
            self._initialized_instances: set = set()
            self._service_lock = threading.Lock()
            self._shutdown_handlers: List[Callable[[], None]] = []

    def register_singleton(self, name: str, instance: Any) -> None:
        with self._service_lock:
            self._services[name] = instance
            self._initialized_instances.add(name)

    def register_factory(self, name: str, factory: Callable[[], Any]) -> None:
        with self._service_lock:
            self._factories[name] = factory

    def register_shutdown_handler(self, handler: Callable[[], None]) -> None:
        with self._service_lock:
            self._shutdown_handlers.append(handler)

    def get(self, name: str) -> Any:
        if name in self._services:
            return self._services[name]

        if name in self._factories:
            with self._service_lock:
                if name in self._factories:
                    instance = self._factories[name]()
                    self._services[name] = instance
                    return instance

        raise KeyError(f"Service '{name}' not found in container")

    def has(self, name: str) -> bool:
        with self._service_lock:
            return name in self._services or name in self._factories

    def initialize_defaults(self) -> None:
        self.register_shutdown_handler(self._shutdown_keyboard_manager)
        self.register_shutdown_handler(self._shutdown_task_queue)
        self.register_shutdown_handler(self._shutdown_capture_manager)

        from config.path_manager import path_manager
        self.register_singleton("path_manager", path_manager)

        from db.sqlite_manager import sqlite_manager
        self.register_singleton("sqlite_manager", sqlite_manager)

        from db.chroma_manager import chroma_manager
        self.register_singleton("chroma_manager", chroma_manager)

        from services.ocr_engine import ocr_engine
        self.register_singleton("ocr_engine", ocr_engine)

        from services.embedding_client import embedding_client
        self.register_singleton("embedding_client", embedding_client)

        from services.ai_client import ai_client
        self.register_singleton("ai_client", ai_client)

        from services.keyboard_manager import keyboard_manager
        self.register_singleton("keyboard_manager", keyboard_manager)

        from core.task_queue import task_queue
        self.register_singleton("task_queue", task_queue)

        from core.capture import capture_manager
        self.register_singleton("capture_manager", capture_manager)

        from config.settings_manager import settings_manager
        self.register_singleton("settings_manager", settings_manager)

    def _shutdown_keyboard_manager(self) -> None:
        if self.has("keyboard_manager"):
            try:
                self.get("keyboard_manager").stop_listening()
            except Exception:
                pass

    def _shutdown_task_queue(self) -> None:
        if self.has("task_queue"):
            try:
                self.get("task_queue").shutdown()
            except Exception:
                pass

    def _shutdown_capture_manager(self) -> None:
        if self.has("capture_manager"):
            try:
                self.get("capture_manager").close()
            except Exception:
                pass

    def shutdown(self) -> None:
        handlers = []
        with self._service_lock:
            handlers = list(reversed(self._shutdown_handlers))

        for handler in handlers:
            try:
                handler()
            except Exception as e:
                print(f"Shutdown handler error: {e}")

        with self._service_lock:
            self._services.clear()
            self._factories.clear()
            self._initialized_instances.clear()


container = DIContainer()
