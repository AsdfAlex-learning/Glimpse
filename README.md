# Glimpse - AI 驱动的桌面级记忆检索系统

一款多模态 AI 驱动的桌面级记忆检索系统，通过"极低门槛的全局截图"与"AI 语义/原生 OCR 双轨分析"，为数字工作者和研究人员构建本地化的"第二大脑"。

## 核心特性

- 📷 **全局快捷键截图** - 毫秒级跨平台屏幕捕获，支持全屏和区域截图
- 🤖 **双轨分析引擎** - AI 语义理解 + 原生 OCR 文本提取，确保信息完整性
- 🔍 **混合检索系统** - FTS5 精确匹配 + ChromaDB 语义搜索，快速定位记忆
- � **绿色便携设计** - 所有数据存储在软件根目录，不污染系统
- ⚡ **UI 绝对流畅** - 严格前后端分离，后台任务异步处理
- 🔒 **数据安全可靠** - 防并发写锁 + 状态机对账，确保数据一致性

## 技术架构

### 核心架构哲学

- **绿色便携，数据主权** - 便携式设计，所有配置、数据库和图片均存储在软件根目录
- **UI 绝对流畅** - 严格前后端分离，主线程仅用于 PySide6 界面渲染
- **极简依赖与务实主义** - 最大限度利用 Python 标准库和 Qt 原生机制

### 系统模块与数据流转

1. **捕获层** - 全局快捷键触发，5 秒防抖 + 10 张强制切分的集群逻辑
2. **消化层** - ThreadPoolExecutor 后台线程池，内存预处理 + 双轨分析
3. **落盘层** - SQLite + ChromaDB 双数据库架构，防并发写锁 + 状态机对账
4. **召回层** - FTS5 精准匹配 + ChromaDB 语义搜索，结果融合排序

### 项目结构

```
Glimpse/
├── main.py                 # 程序唯一入口，初始化 UI、数据库与全局路径
├── config/
│   └── path_manager.py     # 核心路径路由中心，强制所有数据写入 ./GlimpseData
├── ui/                     # 纯前端表现层 (PySide6)
│   ├── main_window.py      # 主窗体与布局
│   └── signals.py          # 跨线程通信的全局信号总线
├── core/                   # 业务逻辑与系统调度
│   ├── capture.py          # pynput 与 mss 的封装，包含集群防抖算法
│   └── task_queue.py       # ThreadPoolExecutor 调度与任务生命周期管理
├── services/               # 外部能力与 API 接入
│   ├── ai_client.py        # 负责打包数据并与云端大模型交互
│   └── ocr_engine.py       # OCR 抽象类与具体实现 (RapidOCR)
├── db/                     # 数据持久化层
│   ├── sqlite_manager.py   # 封装 SQLite CRUD，包含 FTS5 配置与写入互斥锁
│   └── chroma_manager.py   # 封装向量数据库的读写与检索
├── GlimpseData/            # 数据存储目录（自动创建）
│   ├── screenshots/        # 按日期分类的截图存储
│   ├── glimpse.db          # SQLite 数据库
│   └── chroma_db/          # ChromaDB 向量索引
├── requirements.txt        # 项目依赖
└── README.md               # 项目说明
```

## 安装使用

### 环境要求

- Python 3.10+
- Windows 10/11 (支持跨平台)

### 安装步骤

1. **克隆仓库**
```bash
cd D:\ISI\Glimpse
```

2. **创建虚拟环境**
```bash
python -m venv venv
venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **运行应用**
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
1. 捕获屏幕（支持全屏和区域截图）
2. 内存预处理（图片压缩）
3. 双轨分析：
   - 云端 AI 提取核心逻辑与结构化摘要
   - 本地 OCR 提取精确的字符和代码
4. 数据落盘：
   - 图片保存到按日期划分的本地文件夹
   - 元数据写入 SQLite（带 FTS5 索引）
   - 向量嵌入写入 ChromaDB

### 搜索

在搜索框输入自然语言描述或关键词，例如：
- "昨天查看的代码"
- "包含登录页面的截图"
- "微信聊天窗口"
- 具体的代码片段或专有名词

系统会自动进行混合搜索：
- FTS5 路径：精确匹配 OCR 提取的纯文本
- ChromaDB 路径：语义模糊匹配 AI 摘要
- 结果融合：去重、重新打分排序后呈现

### 浏览历史

主窗口的记忆列表按时间倒序显示所有截图，点击可查看详情。

## 技术实现亮点

1. **集群防抖算法** - 5 秒防抖等待 + 10 张强制切分，智能处理高频连续截图
2. **双库协同架构** - SQLite 元数据 + ChromaDB 向量索引，UUID 作为唯一关联键
3. **防并发写锁** - 应用层全局互斥锁，从根源上杜绝 database is locked 崩溃
4. **状态机对账** - sync_status (PENDING/SYNCED/FAILED) 确保数据双写高可用
5. **轻量级 UI 通信** - 后台通过 Qt Signal 仅发送 UUID，UI 异步读取渲染

## 依赖说明

| 类别 | 依赖库 | 用途 |
|------|-------|------|
| **核心 UI** | PySide6 | Qt Python 绑定，界面渲染 |
| **数据库** | ChromaDB | 向量数据库，语义搜索 |
| | sentence-transformers | 文本嵌入模型 |
| **截图** | mss | 跨平台屏幕捕获 |
| | Pillow | 图片处理 |
| | pynput | 全局快捷键监听 |
| **OCR** | rapidocr-onnxruntime | 文字识别 |
| **API** | openai | 大模型接口 |
| | requests | HTTP 请求 |
| | python-dotenv | 环境变量管理 |
| **工具** | psutil | 系统信息 |
| | python-dateutil | 日期时间处理 |

## 开发计划

- [ ] 区域截图功能优化
- [ ] 视频录制支持
- [ ] 标签系统
- [ ] 数据导出/导入
- [ ] 多语言支持
- [ ] 插件系统
- [ ] 本地大模型集成

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可

MIT License

## 致谢

- [PySide6](https://doc.qt.io/qtforpython/) - Qt Python 绑定
- [ChromaDB](https://www.trychroma.com/) - 向量数据库
- [Sentence Transformers](https://www.sbert.net/) - 文本嵌入
- [mss](https://github.com/BoboTiG/python-mss) - 屏幕截图
- [RapidOCR](https://github.com/RapidAI/RapidOCR) - 文字识别
- [pynput](https://github.com/moses-palmer/pynput) - 全局快捷键监听
