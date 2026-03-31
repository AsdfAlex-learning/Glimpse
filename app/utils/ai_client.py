"""
AI 客户端模块 - 多模态 AI 通信

需要写的内容:
1. AIClient 类 (单例)
   - 配置管理 (API Base URL, API Key)
   - OpenAI 客户端初始化
   - 方法:
     - configure (配置客户端)
     - is_configured (检查是否已配置)
     - test_connection (测试 API 连接)
     - analyze_image (分析图片，支持流式输出)
     - generate_summary (生成文本摘要)

2. 全局实例 ai_client

配置项:
- 模型: gpt-4o-mini (或其他支持视觉的模型)
- 最大 tokens: 500
- 温度: 0.7

依赖: openai
"""

from typing import Optional, Callable

# TODO: 导入 openai

# TODO: 定义 AIClient 类

# TODO: 定义全局实例
