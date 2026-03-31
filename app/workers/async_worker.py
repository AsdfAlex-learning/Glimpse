"""
异步任务工作器
负责后台处理图片、AI分析等耗时任务
"""
import asyncio
import threading
from typing import Callable, Optional, Any, Dict
from dataclasses import dataclass
from enum import Enum, auto
from queue import Queue
import time

from app.core.logger import logger


class TaskStatus(Enum):
    """任务状态"""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class Task:
    """任务数据类"""
    id: str
    func: Callable
    args: tuple
    kwargs: dict
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    callback: Optional[Callable] = None
    created_at: float = 0.0
    started_at: Optional[float] = None
    completed_at: Optional[float] = None

    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()

    @property
    def duration(self) -> Optional[float]:
        """获取任务执行时长"""
        if self.started_at is None:
            return None
        end_time = self.completed_at or time.time()
        return end_time - self.started_at

    @property
    def waiting_time(self) -> float:
        """获取等待时间"""
        if self.started_at is None:
            return time.time() - self.created_at
        return self.started_at - self.created_at


class AsyncWorker:
    """异步工作器"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._task_queue: Queue[Task] = Queue()
        self._tasks: Dict[str, Task] = {}
        self._worker_thread: Optional[threading.Thread] = None
        self._running = False
        self._lock = threading.Lock()
        self._task_counter = 0

    def start(self):
        """启动工作器"""
        if self._running:
            logger.warning("AsyncWorker already running")
            return

        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

        logger.info("AsyncWorker started")

    def stop(self):
        """停止工作器"""
        if not self._running:
            return

        self._running = False

        # 清空队列
        while not self._task_queue.empty():
            try:
                task = self._task_queue.get_nowait()
                task.status = TaskStatus.CANCELLED
            except:
                pass

        # 等待工作线程结束
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5.0)

        logger.info("AsyncWorker stopped")

    def _worker_loop(self):
        """工作线程主循环"""
        while self._running:
            try:
                # 获取任务（阻塞，超时1秒）
                task = self._task_queue.get(timeout=1.0)

                if task is None:
                    continue

                # 执行任务
                self._execute_task(task)

            except Exception as e:
                if self._running:  # 只有在运行时记录错误
                    logger.error(f"Worker loop error: {e}")

    def _execute_task(self, task: Task):
        """执行单个任务"""
        with self._lock:
            task.status = TaskStatus.RUNNING
            task.started_at = time.time()

        try:
            # 执行任务函数
            result = task.func(*task.args, **task.kwargs)

            with self._lock:
                task.status = TaskStatus.COMPLETED
                task.result = result
                task.completed_at = time.time()

            logger.info(f"Task completed: {task.id}, duration: {task.duration:.2f}s")

            # 调用回调函数
            if task.callback:
                try:
                    task.callback(task)
                except Exception as e:
                    logger.error(f"Task callback error: {e}")

        except Exception as e:
            with self._lock:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.completed_at = time.time()

            logger.error(f"Task failed: {task.id}, error: {e}")

    def submit(
        self,
        func: Callable,
        *args,
        callback: Optional[Callable[[Task], None]] = None,
        **kwargs,
    ) -> Optional[Task]:
        """
        提交任务到队列

        Args:
            func: 要执行的函数
            *args: 位置参数
            callback: 完成回调函数
            **kwargs: 关键字参数

        Returns:
            Task 对象或 None
        """
        if not self._running:
            logger.error("Cannot submit task: AsyncWorker not running")
            return None

        with self._lock:
            self._task_counter += 1
            task_id = f"task_{self._task_counter}_{int(time.time())}"

        task = Task(
            id=task_id,
            func=func,
            args=args,
            kwargs=kwargs,
            callback=callback,
        )

        # 添加到队列
        self._task_queue.put(task)

        # 保存任务引用
        with self._lock:
            self._tasks[task_id] = task

        logger.info(f"Task submitted: {task_id}")
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务信息"""
        with self._lock:
            return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        with self._lock:
            return list(self._tasks.values())

    def clear_completed_tasks(self):
        """清理已完成的任务"""
        with self._lock:
            completed_status = {TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED}
            self._tasks = {
                k: v for k, v in self._tasks.items()
                if v.status not in completed_status
            }

        logger.info("Completed tasks cleared")

    def is_running(self) -> bool:
        """检查工作器是否运行中"""
        return self._running


# 全局实例
async_worker = AsyncWorker()
