"""
Database模块测试 - sqlite_manager和chroma_manager
"""
import sys
import time
import uuid
from pathlib import Path

project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest


class TestSQLiteManager:
    """测试SQLite管理器"""

    def test_sqlite_manager_init(self):
        """测试SQLite管理器初始化"""
        from db.sqlite_manager import sqlite_manager

        assert sqlite_manager is not None

    def test_insert_memory(self):
        """测试插入记忆"""
        from db.sqlite_manager import sqlite_manager, MemoryRecord

        record = MemoryRecord(
            id=str(uuid.uuid4()),
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            image_path="/fake/path/test.png",
            ai_summary="Test summary",
            app_name="test_app"
        )

        result = sqlite_manager.insert_memory(record)
        assert result is True

        sqlite_manager.delete_memory(record.id)

    def test_get_memory_by_id(self):
        """测试通过ID获取记忆"""
        from db.sqlite_manager import sqlite_manager, MemoryRecord

        record = MemoryRecord(
            id=str(uuid.uuid4()),
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            image_path="/fake/path/test.png",
            ai_summary="Test summary",
            app_name="test_app"
        )

        sqlite_manager.insert_memory(record)

        retrieved = sqlite_manager.get_memory_by_id(record.id)
        assert retrieved is not None
        assert retrieved.id == record.id
        assert retrieved.ai_summary == "Test summary"

        sqlite_manager.delete_memory(record.id)

    def test_get_all_memories(self):
        """测试获取所有记忆"""
        from db.sqlite_manager import sqlite_manager

        memories = sqlite_manager.get_all_memories(limit=10)
        assert isinstance(memories, list)

    def test_search_memories(self):
        """测试搜索记忆"""
        from db.sqlite_manager import sqlite_manager, MemoryRecord

        unique_id = str(uuid.uuid4())[:8]
        record = MemoryRecord(
            id=f"search_test_{unique_id}",
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            image_path="/fake/path/test.png",
            ai_summary=f"SearchableContent_{unique_id}",
            app_name="test_app"
        )

        sqlite_manager.insert_memory(record)

        results = sqlite_manager.search_memories(f"SearchableContent_{unique_id}")
        found = any(r.id == record.id for r in results)
        assert found is True

        sqlite_manager.delete_memory(record.id)

    def test_update_memory_summary(self):
        """测试更新记忆摘要"""
        from db.sqlite_manager import sqlite_manager, MemoryRecord

        record = MemoryRecord(
            id=str(uuid.uuid4()),
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            image_path="/fake/path/test.png",
            ai_summary="Original summary",
            app_name="test_app"
        )

        sqlite_manager.insert_memory(record)

        result = sqlite_manager.update_memory_summary(record.id, "Updated summary")
        assert result is True

        updated = sqlite_manager.get_memory_by_id(record.id)
        assert updated.ai_summary == "Updated summary"

        sqlite_manager.delete_memory(record.id)

    def test_delete_memory(self):
        """测试删除记忆"""
        from db.sqlite_manager import sqlite_manager, MemoryRecord

        record = MemoryRecord(
            id=str(uuid.uuid4()),
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
            image_path="/fake/path/test.png",
            ai_summary="To be deleted",
            app_name="test_app"
        )

        sqlite_manager.insert_memory(record)

        result = sqlite_manager.delete_memory(record.id)
        assert result is True

        retrieved = sqlite_manager.get_memory_by_id(record.id)
        assert retrieved is None

    def test_get_memories_count(self):
        """测试获取记忆数量"""
        from db.sqlite_manager import sqlite_manager

        count = sqlite_manager.get_memories_count()
        assert isinstance(count, int)
        assert count >= 0


class TestChromaManager:
    """测试ChromaDB管理器"""

    def test_chroma_manager_init(self):
        """测试ChromaDB管理器初始化"""
        from db.chroma_manager import chroma_manager

        assert chroma_manager is not None

    def test_add_and_search(self):
        """测试添加和搜索"""
        from db.chroma_manager import chroma_manager

        test_id = str(uuid.uuid4())
        embedding = [0.1] * 384

        result = chroma_manager.add(test_id, embedding, {"text": "test content"})
        assert result is True

        results = chroma_manager.search([0.1] * 384, n_results=1)
        assert results is not None

        chroma_manager.delete(test_id)

    def test_delete(self):
        """测试删除"""
        from db.chroma_manager import chroma_manager

        test_id = str(uuid.uuid4())
        embedding = [0.2] * 384

        chroma_manager.add(test_id, embedding, {"text": "to delete"})

        result = chroma_manager.delete(test_id)
        assert result is True

    def test_get_collection_count(self):
        """测试获取集合数量"""
        from db.chroma_manager import chroma_manager

        count = chroma_manager.get_collection_count()
        assert isinstance(count, int)
        assert count >= 0
