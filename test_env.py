"""
环境验证脚本
用于验证Glimpse项目的环境配置是否正确
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def test_python_version():
    """测试Python版本"""
    print("=== 测试Python版本 ===")
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor in (10, 13):
        print(f"OK: Python版本满足要求 (3.{version.minor}.{version.micro})")
        return True
    else:
        print("FAIL: Python环境版本错误，需要 3.10.x 或 3.13.x")
        return False


def test_dependencies():
    """测试依赖安装情况"""
    print("\n=== 测试依赖安装 ===")
    
    # 正确映射：包名 → 导入名
    package_import_map = {
        'PySide6': 'PySide6',
        'chromadb': 'chromadb',
        'sentence-transformers': 'sentence_transformers',
        'transformers': 'transformers',
        'huggingface_hub': 'huggingface_hub',
        'tokenizers': 'tokenizers',
        'numpy': 'numpy',
        'mss': 'mss',
        'Pillow': 'PIL',
        'pynput': 'pynput',
        'rapidocr-onnxruntime': 'rapidocr_onnxruntime',
        'openai': 'openai',
        'requests': 'requests',
        'python-dotenv': 'dotenv',
        'psutil': 'psutil',
        'python-dateutil': 'dateutil',
        'pytest': 'pytest',
        'pytest-qt': 'pytestqt',
        'pytest-cov': 'pytest_cov',
        'certifi': 'certifi',
        'charset_normalizer': 'charset_normalizer',
        'idna': 'idna',
        'urllib3': 'urllib3'
    }
    
    missing_packages = []
    
    for package, import_name in package_import_map.items():
        try:
            module = __import__(import_name)
            version = getattr(module, "__version__", "unknown")
            print(f"OK: {package} 已安装 (版本: {version})")
            
            if package == "Pillow":
                from PIL import Image
                print("  - Pillow: 测试成功")
            elif package == "requests":
                print("  - requests: 测试成功")
            elif package == "psutil":
                import psutil
                print(f"  - psutil: 系统CPU使用率: {psutil.cpu_percent():.1f}%")
        except ImportError:
            missing_packages.append(package)
            print(f"FAIL: {package} 未安装")
    
    if missing_packages:
        print(f"\nERROR: 缺少以下依赖: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("\nOK: 所有依赖都已正确安装")
        return True


def test_module_imports():
    """测试模块导入"""
    print("\n=== 测试模块导入 ===")

    modules = [
        'config.path_manager',
        'config.settings_manager',
        'ui.main_window',
        'ui.signals',
        'ui.settings_dialog',
        'core.capture',
        'core.task_queue',
        'services.ai_client',
        'services.ocr_engine',
        'services.keyboard_manager',
        'services.embedding_client',
        'db.sqlite_manager',
        'db.chroma_manager'
    ]

    import_errors = []

    for module in modules:
        try:
            __import__(module)
            print(f"OK: {module} 导入成功")
        except Exception as e:
            import_errors.append((module, str(e)))
            print(f"FAIL: {module} 导入失败: {e}")

    if import_errors:
        print("\nERROR: 部分模块导入失败")
        for module, error in import_errors:
            print(f"  - {module}: {error}")
        return False
    else:
        print("\nOK: 所有模块导入成功")
        return True


def test_path_manager():
    """测试路径管理器"""
    print("\n=== 测试路径管理器 ===")

    try:
        from config.path_manager import path_manager
        print("OK: 路径管理器初始化成功")
        print(f"  - 数据目录: {path_manager.data_root}")
        print(f"  - 截图目录: {path_manager.screenshots_dir}")
        print(f"  - SQLite路径: {path_manager.sqlite_path}")
        print(f"  - ChromaDB路径: {path_manager.chroma_path}")
        return True
    except Exception as e:
        print(f"FAIL: 路径管理器测试失败: {e}")
        return False


def test_settings_manager():
    """测试设置管理器"""
    print("\n=== 测试设置管理器 ===")

    try:
        from config.settings_manager import settings_manager
        print("OK: 设置管理器初始化成功")

        settings = settings_manager.get_all()
        print(f"  - 获取全部设置: 成功 ({len(settings)} 个顶级键)")

        hotkey = settings_manager.get("hotkeys.screenshot")
        print(f"  - 获取快捷键配置: {hotkey}")

        debounce = settings_manager.get("screenshot.debounce_interval")
        print(f"  - 获取截图配置: 防抖间隔={debounce}")

        return True
    except Exception as e:
        print(f"FAIL: 设置管理器测试失败: {e}")
        return False


def test_database_connections():
    """测试数据库连接"""
    print("\n=== 测试数据库连接 ===")

    try:
        from db.sqlite_manager import sqlite_manager
        print("OK: SQLite 连接成功")
        count = sqlite_manager.get_memories_count()
        print(f"  - 当前记忆数量: {count}")
    except Exception as e:
        print(f"FAIL: SQLite 连接测试失败: {e}")
        return False

    try:
        from db.chroma_manager import chroma_manager
        print("OK: ChromaDB 连接成功")
    except Exception as e:
        print(f"FAIL: ChromaDB 连接测试失败: {e}")
        return False

    return True


def test_service_instances():
    """测试服务实例化"""
    print("\n=== 测试服务实例 ===")

    results = []

    try:
        from services.ocr_engine import ocr_engine
        print(f"OK: OCR Engine 实例化成功")
        print(f"  - 引擎类型: {type(ocr_engine).__name__}")
    except Exception as e:
        print(f"FAIL: OCR Engine 实例化失败: {e}")
        results.append(False)

    try:
        from services.keyboard_manager import keyboard_manager
        print(f"OK: Keyboard Manager 实例化成功")
        print(f"  - 运行状态: {keyboard_manager.is_running()}")
    except Exception as e:
        print(f"FAIL: Keyboard Manager 实例化失败: {e}")
        results.append(False)

    try:
        from core.capture import capture_manager
        print(f"OK: Capture Manager 实例化成功")
        settings = capture_manager.get_settings()
        print(f"  - 截图设置: 防抖={settings['debounce_interval']}s")
    except Exception as e:
        print(f"FAIL: Capture Manager 实例化失败: {e}")
        results.append(False)

    try:
        from core.task_queue import task_queue
        print(f"OK: Task Queue 实例化成功")
        print(f"  - 队列状态: 运行中")
    except Exception as e:
        print(f"FAIL: Task Queue 实例化失败: {e}")
        results.append(False)

    return all(results) if results else True


def main():
    """主测试函数"""
    print("=== 开始环境验证 ===\n")

    tests = [
        test_python_version,
        test_dependencies,
        test_module_imports,
        test_path_manager,
        test_settings_manager,
        test_database_connections,
        test_service_instances,
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "="*50)
    print("=== 环境验证结果 ===")
    print("="*50)

    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"通过: {passed}/{total}")

    if all(results):
        print("OK: 所有测试通过！环境配置正确。")
        print("\n你可以运行: python main.py 来启动应用")
        return 0
    else:
        print("FAIL: 部分测试失败，请检查环境配置。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
