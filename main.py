"""
Glimpse - AI 驱动的桌面级记忆检索系统
程序唯一入口，初始化 UI、数据库与全局路径

启动顺序：
1. 初始化路径（path_manager）
2. 初始化数据库（sqlite + chroma）
3. 初始化服务（ocr、embedding）
4. 初始化任务队列
5. 启动 UI

这里仅仅是AI生成的代码，具体实例名称等内容以实际代码为准
仅展示启动顺序，不代表实际代码中的顺序或实例名称
"""
import sys

import os
from pathlib import Path

project_root = Path(__file__).parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication


def main():
    # 1. 初始化路径（path_manager）
    print("Initializing path manager...")
    from config.path_manager import path_manager
    
    # 2. 初始化数据库（sqlite + chroma）
    print("Initializing databases...")
    from db.sqlite_manager import SQLiteManager
    from db.chroma_manager import ChromaManager
    
    sqlite_manager = SQLiteManager()
    chroma_manager = ChromaManager()
    
    # 3. 初始化服务（ocr、embedding）
    print("Initializing services...")
    from services.ocr_engine import OCREngine
    from services.embedding_client import EmbeddingClient
    
    ocr_engine = OCREngine()
    embedding_client = EmbeddingClient()
    
    # 4. 初始化任务队列
    print("Initializing task queue...")
    from core.task_queue import TaskQueueManager
    
    task_queue = TaskQueueManager()
    
    # 5. 启动 UI
    print("Starting UI...")
    app = QApplication(sys.argv)
    app.setApplicationName("Glimpse")
    app.setOrganizationName("Glimpse")
    
    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
