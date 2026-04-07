"""
Core模块测试 - capture和task_queue
"""
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest


class TestCaptureManager:
    """测试截图管理器"""

    def test_capture_manager_init(self):
        """测试截图管理器初始化"""
        from core.capture import capture_manager

        assert capture_manager is not None

    def test_get_settings(self):
        """测试获取设置"""
        from core.capture import capture_manager

        settings = capture_manager.get_settings()
        assert "debounce_interval" in settings
        assert "cluster_threshold" in settings
        assert "max_captures_per_window" in settings

    def test_update_settings(self):
        """测试更新设置"""
        from core.capture import capture_manager

        old_settings = capture_manager.get_settings()

        new_settings = {
            "debounce_interval": 10.0,
            "cluster_threshold": 3.0,
            "max_captures_per_window": 20
        }

        result = capture_manager.update_settings(new_settings)
        assert result is True

        updated = capture_manager.get_settings()
        assert updated["debounce_interval"] == 10.0
        assert updated["cluster_threshold"] == 3.0
        assert updated["max_captures_per_window"] == 20

        capture_manager.update_settings(old_settings)

    def test_update_settings_invalid(self):
        """测试更新无效设置"""
        from core.capture import capture_manager

        result = capture_manager.update_settings({
            "debounce_interval": -5.0
        })
        assert result is False

        result = capture_manager.update_settings({
            "max_captures_per_window": 0
        })
        assert result is False

    def test_set_debounce_interval(self):
        """测试设置防抖间隔"""
        from core.capture import capture_manager

        assert capture_manager.set_debounce_interval(7.5) is True
        assert capture_manager.set_debounce_interval(0) is False
        assert capture_manager.set_debounce_interval(-1) is False

    def test_set_cluster_threshold(self):
        """测试设置集群阈值"""
        from core.capture import capture_manager

        assert capture_manager.set_cluster_threshold(4.0) is True
        assert capture_manager.set_cluster_threshold(0) is False

    def test_set_max_captures(self):
        """测试设置最大截图数"""
        from core.capture import capture_manager

        assert capture_manager.set_max_captures_per_window(50) is True
        assert capture_manager.set_max_captures_per_window(0) is False

    def test_capture_count_tracking(self):
        """测试截图计数跟踪"""
        from core.capture import capture_manager

        capture_manager.update_settings({
            "max_captures_per_window": 5
        })

        for _ in range(3):
            capture_manager._update_capture_count(is_fullscreen=True)

        assert capture_manager._fullscreen_count == 3


class TestTaskQueue:
    """测试任务队列"""

    def test_task_queue_init(self):
        """测试任务队列初始化"""
        from core.task_queue import task_queue

        assert task_queue is not None

    def test_submit_task(self):
        """测试提交任务"""
        from core.task_queue import task_queue

        def simple_task():
            return 1 + 1

        task_id = task_queue.submit(simple_task)
        assert task_id is not None

        task_queue.wait_for_tasks_completion(timeout=5.0)

    def test_submit_multiple_tasks(self):
        """测试提交多个任务"""
        from core.task_queue import task_queue

        def task(n):
            time.sleep(0.1)
            return n * 2

        ids = []
        for i in range(5):
            tid = task_queue.submit(task, args=(i,))
            ids.append(tid)

        completed = task_queue.wait_for_tasks_completion(timeout=10.0)
        assert completed is True

    def test_cancel_pending(self):
        """测试取消待处理任务"""
        from core.task_queue import task_queue

        def long_task():
            time.sleep(10)
            return 1

        def short_task():
            return 2

        task_queue.submit(long_task)
        task_queue.submit(short_task)

        cancelled = task_queue.cancel_all_pending()
        assert cancelled >= 0

    def test_shutdown(self):
        """测试关闭"""
        from core.task_queue import task_queue

        task_queue.shutdown()

        with pytest.raises(RuntimeError):
            task_queue.submit(lambda: 1)

    def test_task_status(self):
        """测试任务状态"""
        from core.task_queue import task_queue, TaskStatus

        def quick_task():
            return 1

        task_id = task_queue.submit(quick_task)
        task_queue.wait_for_tasks_completion(timeout=5.0)

        task = task_queue._tasks.get(task_id)
        if task:
            assert task.status == TaskStatus.COMPLETED