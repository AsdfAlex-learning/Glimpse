"""
SQLite 数据库模块 - 元数据存储

需要写的内容:
1. MemoryRecord 数据类
   - 字段: id, created_at, image_path, ai_summary, app_name
   - 序列化/反序列化方法

2. SQLiteManager 类 (单例)
   - 数据库连接管理
   - 表创建/初始化
   - CRUD 操作:
     - insert_memory
     - get_memory_by_id
     - get_all_memories
     - search_memories (文本搜索)
     - update_memory_summary
     - delete_memory
     - get_memories_count

3. 全局实例 sqlite_manager
"""

import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

# TODO: 定义 MemoryRecord 数据类

# TODO: 定义 SQLiteManager 类

# TODO: 定义全局实例
