"""
Config模块测试 - path_manager和settings_manager
"""
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest


class TestPathManager:
    """测试路径管理器"""

    def test_path_manager_init(self):
        """测试路径管理器初始化"""
        from config.path_manager import path_manager

        assert path_manager is not None
        assert path_manager.data_root.exists()

    def test_screenshots_dir(self):
        """测试截图目录"""
        from config.path_manager import path_manager

        assert path_manager.screenshots_dir.exists()

    def test_sqlite_path(self):
        """测试SQLite路径"""
        from config.path_manager import path_manager

        assert path_manager.sqlite_path.parent.exists()

    def test_chroma_path(self):
        """测试ChromaDB路径"""
        from config.path_manager import path_manager

        assert path_manager.chroma_path.parent.exists()

    def test_screenshot_path_generation(self):
        """测试截图路径生成"""
        from config.path_manager import path_manager

        path = path_manager.get_screenshot_path("test.png")
        assert path.parent == path_manager.screenshots_dir


class TestSettingsManager:
    """测试设置管理器"""

    def test_settings_manager_init(self):
        """测试设置管理器初始化"""
        from config.settings_manager import settings_manager

        assert settings_manager is not None

    def test_get_all(self):
        """测试获取所有设置"""
        from config.settings_manager import settings_manager

        settings = settings_manager.get_all()
        assert isinstance(settings, dict)
        assert "hotkeys" in settings
        assert "screenshot" in settings
        assert "ai" in settings
        assert "ocr" in settings
        assert "database" in settings
        assert "ui" in settings

    def test_get_with_dot_notation(self):
        """测试点号路径获取"""
        from config.settings_manager import settings_manager

        hotkey = settings_manager.get("hotkeys.screenshot")
        assert hotkey is not None
        assert isinstance(hotkey, str)

    def test_get_with_default(self):
        """测试获取默认值"""
        from config.settings_manager import settings_manager

        value = settings_manager.get("nonexistent.key", "default_value")
        assert value == "default_value"

    def test_has_changes(self):
        """测试变化检测"""
        from config.settings_manager import settings_manager

        current = settings_manager.get_all()
        assert not settings_manager.has_changes(current)

        modified = current.copy()
        modified["hotkeys"]["screenshot"] = "<ctrl>+<shift>+x"
        assert settings_manager.has_changes(modified)

    def test_update_and_rollback(self):
        """测试更新和回滚"""
        from config.settings_manager import settings_manager

        original = settings_manager.get_all()
        original_debounce = original["screenshot"]["debounce_interval"]
        original_cluster = original["screenshot"]["cluster_threshold"]
        original_max = original["screenshot"]["max_captures_per_window"]

        new_settings = {
            "screenshot": {
                "debounce_interval": 99.0,
                "cluster_threshold": original_cluster,
                "max_captures_per_window": original_max
            }
        }

        success = settings_manager.update(new_settings)
        assert success, "update() should return True with complete screenshot config"

        new_debounce = settings_manager.get("screenshot.debounce_interval")
        assert new_debounce == 99.0

        settings_manager.update({
            "screenshot": {
                "debounce_interval": original_debounce,
                "cluster_threshold": original_cluster,
                "max_captures_per_window": original_max
            }
        })

        restored = settings_manager.get("screenshot.debounce_interval")
        assert restored == original_debounce

    def test_validation(self):
        """测试配置验证"""
        from config.settings_manager import settings_manager

        original = settings_manager.get_all()
        original_cluster = original["screenshot"]["cluster_threshold"]
        original_max = original["screenshot"]["max_captures_per_window"]

        invalid_settings = {
            "screenshot": {
                "debounce_interval": -5.0,
                "cluster_threshold": original_cluster,
                "max_captures_per_window": original_max
            }
        }

        result = settings_manager.update(invalid_settings)
        assert result is False

    def test_reset(self):
        """测试重置为默认"""
        from config.settings_manager import settings_manager

        original = settings_manager.get_all()

        settings_manager.update({
            "screenshot": {
                "debounce_interval": 99.0,
                "cluster_threshold": original["screenshot"]["cluster_threshold"],
                "max_captures_per_window": original["screenshot"]["max_captures_per_window"]
            }
        })

        settings_manager.reset()

        assert settings_manager.get("screenshot.debounce_interval") == 5.0
