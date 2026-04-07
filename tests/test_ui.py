"""
UI模块测试 - main_window和settings_dialog
"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest


class TestSignals:
    """测试信号系统"""

    def test_signals_import(self):
        """测试信号导入"""
        from ui.signals import signals

        assert signals is not None

    def test_signals_exist(self):
        """测试信号存在"""
        from ui.signals import signals

        required_signals = [
            "screenshot_requested",
            "screenshot_completed",
            "memory_saved",
            "search_completed",
            "error_occurred",
            "status_updated"
        ]

        for sig_name in required_signals:
            assert hasattr(signals, sig_name), f"Signal {sig_name} not found"


class TestSettingsDialog:
    """测试设置对话框"""

    def test_settings_dialog_import(self):
        """测试设置对话框导入"""
        from ui.settings_dialog import SettingsDialog

        assert SettingsDialog is not None

    def test_hotkey_pattern(self):
        """测试快捷键正则"""
        from ui.settings_dialog import SettingsDialog
        import re

        pattern = SettingsDialog.HOTKEY_PATTERN

        valid_hotkeys = [
            "<ctrl>+<shift>+g",
            "<ctrl>+f",
            "<escape>",
            "ctrl+c",
            "a",
            "<ctrl>+<alt>+<shift>+x"
        ]

        for hotkey in valid_hotkeys:
            assert pattern.match(hotkey), f"Valid hotkey {hotkey} should match"

        invalid_hotkeys = [
            "<ctrl>",
            "+g",
            "ctrl++shift+g",
            ""
        ]

        for hotkey in invalid_hotkeys:
            if hotkey:
                assert not pattern.match(hotkey), f"Invalid hotkey {hotkey} should not match"
