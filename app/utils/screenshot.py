"""
屏幕截图模块

需要写的内容:
1. ScreenshotManager 类 (单例)
   - mss 初始化
   - 截图方法:
     - capture_fullscreen (全屏截图，支持延迟)
     - capture_region (区域截图)
   - 图片压缩方法:
     - _compress_image (JPEG 压缩，支持质量、最大宽度)
   - 图片保存方法
   - 资源清理 (close)

2. 全局实例 screenshot_manager

依赖: mss, Pillow
"""

from pathlib import Path
from typing import Optional, Tuple

# TODO: 导入 mss, PIL.Image

# TODO: 定义 ScreenshotManager 类

# TODO: 定义全局实例
