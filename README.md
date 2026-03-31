# Glimpse - AI 桌面记忆助手

一个智能的桌面截图记忆工具，能够自动捕获屏幕、AI 分析内容，并通过自然语言搜索快速检索历史记忆。

## 功能特性

- 📷 **一键截图** - 全局快捷键捕获屏幕，自动分析图片内容
- 🤖 **AI 智能分析** - 使用多模态 AI 自动生成图片描述
- 🔍 **自然语言搜索** - 通过向量数据库实现语义搜索
- 🖥️ **系统托盘** - 后台运行，随时可用
- 🎨 **浅色/深色主题** - 支持自动切换

## 技术架构

```
Glimpse/
├── app/
│   ├── core/           # 核心模块
│   │   ├── config.py      # 配置常量
│   │   ├── logger.py      # 日志系统
│   │   └── settings.py    # 设置管理
│   ├── db/             # 数据库模块
│   │   ├── sqlite_db.py   # SQLite 管理
│   │   ├── chroma_db.py   # ChromaDB 管理
│   │   └── embedding.py   # 向量嵌入
│   ├── ui/             # UI 模块
│   │   ├── main_window.py # 主窗口
│   │   └── styles.py      # 样式主题
│   ├── utils/          # 工具模块
│   │   ├── screenshot.py  # 截图工具
│   │   ├── hotkey.py      # 快捷键监听
│   │   ├── ai_client.py   # AI 客户端
│   │   └── helpers.py     # 辅助函数
│   └── workers/        # 工作线程
│       ├── async_worker.py # 异步任务
│       └── ai_processor.py # AI 处理流程
├── data/               # 数据目录
│   ├── screenshots/    # 截图存储
│   ├── glimpse.db      # SQLite 数据库
│   └── chroma_db/      # ChromaDB 数据
├── assets/             # 资源文件
│   └── icons/          # 图标
├── tests/              # 测试目录
├── main.py             # 启动入口
├── requirements.txt    # 依赖列表
└── README.md           # 项目说明
```

## 安装使用

### 环境要求

- Python 3.10+
- Windows 10/11 (目前主要支持 Windows)

### 安装步骤

1. 克隆仓库
```bash
cd D:\ISI\Glimpse
```

2. 创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行应用
```bash
python main.py
```

### 首次配置

1. 打开应用后，点击"设置"按钮
2. 配置 API Base URL 和 API Key
   - 支持 OpenAI 格式的 API
   - 或使用兼容的第三方服务
3. 测试连接成功后保存设置
4. 配置全局快捷键（默认 `Ctrl+Shift+G`）

## 使用指南

### 截图

- **方式一**：点击主窗口的"📷 截图"按钮
- **方式二**：使用全局快捷键 `Ctrl+Shift+G`

截图后，应用会自动：
1. 捕获屏幕
2. 调用 AI 分析图片内容
3. 生成向量嵌入
4. 保存到数据库

### 搜索

在搜索框输入自然语言描述，例如：
- "昨天查看的代码"
- "包含登录页面的截图"
- "微信聊天窗口"

系统会自动进行语义搜索，返回最相关的结果。

### 浏览历史

主窗口的记忆列表按时间倒序显示所有截图，点击可查看详情。

## 开发计划

- [ ] 区域截图功能
- [ ] 视频录制支持
- [ ] OCR 文字识别
- [ ] 标签系统
- [ ] 数据导出/导入
- [ ] 多语言支持
- [ ] 插件系统

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可

MIT License

## 致谢

- [PySide6](https://doc.qt.io/qtforpython/) - Qt Python 绑定
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [Sentence Transformers](https://www.sbert.net/) - 文本嵌入
- [mss](https://github.com/BoboTiG/python-mss) - 屏幕截图
