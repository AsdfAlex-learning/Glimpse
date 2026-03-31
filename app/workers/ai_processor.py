"""
AI 处理工作流模块
负责协调截图、AI分析、数据存储的完整流程
"""
import io
from typing import Optional, Callable
from pathlib import Path
from datetime import datetime

from PIL import Image

from app.core.config import DEFAULT_SETTINGS
from app.core.logger import logger
from app.core.settings import settings_manager
from app.db.sqlite_db import sqlite_manager, MemoryRecord
from app.db.chroma_db import chroma_manager
from app.db.embedding import embedding_manager
from app.utils.screenshot import screenshot_manager
from app.utils.ai_client import ai_client
from app.utils.helpers import get_active_window_info
from app.workers.async_worker import async_worker, Task


class AIProcessor:
    """AI 处理器"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._processing = False

    def process_screenshot(
        self,
        progress_callback: Optional[Callable[[str], None]] = None,
        completion_callback: Optional[Callable[[bool, MemoryRecord], None]] = None,
    ) -> Optional[Task]:
        """
        处理截图的完整工作流

        Args:
            progress_callback: 进度回调，接收状态消息
            completion_callback: 完成回调，接收成功标志和记忆记录

        Returns:
            Task 对象
        """
        def _progress(msg: str):
            logger.info(msg)
            if progress_callback:
                progress_callback(msg)

        def _workflow():
            """实际工作流"""
            try:
                self._processing = True
                settings = settings_manager.get_settings()

                # 1. 截图
                _progress("正在截图...")
                result = screenshot_manager.capture_fullscreen(
                    delay=settings.screenshot_delay,
                    compress=True,
                )

                if result is None:
                    raise Exception("截图失败")

                pil_img, img_bytes = result
                _progress("截图完成")

                # 2. 获取当前应用信息
                window_info = get_active_window_info()
                app_name = window_info.get("app_name", "Unknown")
                _progress(f"当前应用: {app_name}")

                # 3. 保存图片到文件
                timestamp = datetime.now()
                filename = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{uuid_str()[:8]}.jpg"
                storage_path = Path(settings.storage_path)
                storage_path.mkdir(parents=True, exist_ok=True)

                image_path = storage_path / filename
                screenshot_manager.save_image(img_bytes, image_path)
                _progress(f"图片已保存: {image_path}")

                # 4. 创建记忆记录
                memory = MemoryRecord(
                    created_at=timestamp,
                    image_path=str(image_path.relative_to(storage_path.parent) if
                               image_path.is_relative_to(storage_path.parent)
                               else image_path),
                    ai_summary="",  # 暂时为空，等待AI分析
                    app_name=app_name,
                )

                # 5. 保存到 SQLite
                if not sqlite_manager.insert_memory(memory):
                    raise Exception("保存记忆到数据库失败")
                _progress("记忆已保存到数据库")

                # 6. 调用 AI 分析图片
                _progress("正在分析图片...")

                # 检查 AI 客户端是否已配置
                if not ai_client.is_configured():
                    _progress("AI 客户端未配置，跳过分析")
                    ai_summary = "（AI 未配置，无法分析）"
                else:
                    # 使用压缩后的图片进行 AI 分析
                    ai_summary = ai_client.analyze_image(
                        image_data=img_bytes,
                        prompt="请用中文详细描述这张图片的内容，包括：1. 画面中的主要元素；2. 文字内容（如果有）；3. 整体场景或用途。",
                    )

                    if ai_summary is None:
                        ai_summary = "（AI 分析失败）"

                _progress(f"AI 分析完成: {ai_summary[:100]}...")

                # 7. 更新 SQLite 中的 AI 总结
                sqlite_manager.update_memory_summary(memory.id, ai_summary)

                # 8. 生成嵌入向量并保存到 ChromaDB
                _progress("正在生成向量嵌入...")
                embedding = embedding_manager.encode(ai_summary)

                if embedding:
                    chroma_manager.add_memory(
                        memory_id=memory.id,
                        text=ai_summary,
                        embedding=embedding,
                        metadata={
                            "created_at": memory.created_at.isoformat(),
                            "app_name": app_name,
                        }
                    )
                    _progress("向量嵌入已保存")
                else:
                    _progress("向量嵌入生成失败")

                # 更新记忆记录的 AI 总结
                memory.ai_summary = ai_summary

                _progress("处理完成！")
                return memory

            except Exception as e:
                logger.exception("Error in AI processing workflow")
                _progress(f"处理失败: {str(e)}")
                raise
            finally:
                self._processing = False

        # 提交到异步工作器
        def _on_complete(task: Task):
            if completion_callback:
                success = task.status.name == "COMPLETED"
                memory = task.result if success else None
                completion_callback(success, memory)

        return async_worker.submit(
            _workflow,
            callback=_on_complete,
        )

    def is_processing(self) -> bool:
        """检查是否正在处理中"""
        return self._processing


def uuid_str() -> str:
    """生成 UUID 字符串"""
    import uuid
    return str(uuid.uuid4()).replace("-", "")


# 全局实例
ai_processor = AIProcessor()
