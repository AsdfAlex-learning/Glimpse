"""
Services模块测试 - keyboard_manager, ocr_engine, ai_client, embedding_client
"""
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest


class TestKeyboardManager:
    """测试键盘管理器"""

    def test_keyboard_manager_init(self):
        """测试键盘管理器初始化"""
        from services.keyboard_manager import keyboard_manager

        assert keyboard_manager is not None

    def test_register_hotkey(self):
        """测试注册快捷键"""
        from services.keyboard_manager import keyboard_manager

        def dummy_callback():
            pass

        keyboard_manager.register_hotkey("<ctrl>+<shift>+t", dummy_callback)
        hotkeys = keyboard_manager.get_hotkeys()
        assert "<ctrl>+<shift>+t" in hotkeys

        keyboard_manager.unregister_hotkey("<ctrl>+<shift>+t")

    def test_unregister_hotkey(self):
        """测试注销快捷键"""
        from services.keyboard_manager import keyboard_manager

        def dummy_callback():
            pass

        keyboard_manager.register_hotkey("<ctrl>+<shift>+u", dummy_callback)
        keyboard_manager.unregister_hotkey("<ctrl>+<shift>+u")

        hotkeys = keyboard_manager.get_hotkeys()
        assert "<ctrl>+<shift>+u" not in hotkeys

    def test_clear_hotkeys(self):
        """测试清空快捷键"""
        from services.keyboard_manager import keyboard_manager

        def dummy_callback():
            pass

        keyboard_manager.register_hotkey("<ctrl>+a", dummy_callback)
        keyboard_manager.register_hotkey("<ctrl>+b", dummy_callback)

        keyboard_manager.clear_hotkeys()

        hotkeys = keyboard_manager.get_hotkeys()
        assert len(hotkeys) == 0

    def test_reload_hotkeys(self):
        """测试重新加载快捷键"""
        from services.keyboard_manager import keyboard_manager

        def new_callback():
            pass

        new_hotkeys = {"<ctrl>+<shift>+r": new_callback}

        result = keyboard_manager.reload_hotkeys(new_hotkeys)
        assert isinstance(result, bool)

        hotkeys = keyboard_manager.get_hotkeys()
        assert "<ctrl>+<shift>+r" in hotkeys

    def test_is_running(self):
        """测试运行状态"""
        from services.keyboard_manager import keyboard_manager

        initial_state = keyboard_manager.is_running()
        assert isinstance(initial_state, bool)

    def test_listener_lifecycle(self):
        """测试监听器生命周期"""
        from services.keyboard_manager import keyboard_manager

        keyboard_manager.stop_listening()
        assert keyboard_manager.is_running() is False

        keyboard_manager.start_listening()
        time.sleep(0.5)

        keyboard_manager.stop_listening()
        assert keyboard_manager.is_running() is False


class TestOCREngine:
    """测试OCR引擎"""

    def test_ocr_engine_init(self):
        """测试OCR引擎初始化"""
        from services.ocr_engine import ocr_engine

        assert ocr_engine is not None

    def test_ocr_engine_type(self):
        """测试OCR引擎类型"""
        from services.ocr_engine import ocr_engine

        assert type(ocr_engine).__name__ in ["RapidOCREngine", "NativeOCREngine"]

    def test_extract_text_invalid(self):
        """测试提取无效图片"""
        from services.ocr_engine import ocr_engine

        result = ocr_engine.extract_text("nonexistent_image.png")
        assert result is None

    def test_extract_text_boxes_invalid(self):
        """测试提取无效图片的文本框"""
        from services.ocr_engine import ocr_engine

        result = ocr_engine.extract_text_boxes("nonexistent_image.png")
        assert result == []


class TestEmbeddingClient:
    """测试Embedding客户端"""

    def test_embedding_client_init(self):
        """测试embedding客户端初始化"""
        from services.embedding_client import embedding_client

        assert embedding_client is not None

    def test_get_embedding(self):
        """测试获取embedding"""
        from services.embedding_client import embedding_client

        result = embedding_client.get_embedding("test text")
        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0


class TestAIClient:
    """测试AI客户端"""

    def test_ai_client_init(self):
        """测试AI客户端初始化"""
        from services.ai_client import ai_client

        assert ai_client is not None

    def test_is_configured(self):
        """测试配置状态"""
        from services.ai_client import ai_client

        configured = ai_client.is_configured()
        assert isinstance(configured, bool)

    def test_configure(self):
        """测试配置"""
        from services.ai_client import ai_client

        ai_client.configure(api_key="test_key")
        assert ai_client.is_configured() is True

    def test_analyze_image_without_config(self):
        """测试未配置时分析图片"""
        from services.ai_client import ai_client

        ai_client._client = None

        with pytest.raises(RuntimeError):
            ai_client.analyze_image("test.png")

    def test_generate_summary_without_config(self):
        """测试未配置时生成摘要"""
        from services.ai_client import ai_client

        ai_client._client = None

        with pytest.raises(RuntimeError):
            ai_client.generate_summary("test text")
