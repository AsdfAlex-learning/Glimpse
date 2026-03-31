# Glimpse 环境配置指南

本文档介绍如何设置 Glimpse 的开发环境。

## 环境要求

- **Python**: 3.10 或更高版本
- **操作系统**: macOS / Linux / Windows

## 依赖说明

| 类别 | 依赖 | 说明 |
|------|------|------|
| **UI** | PySide6==6.6.1 | Qt for Python GUI 框架 |
| **数据库** | chromadb, sqlite | 向量数据库 + SQL 数据库 |
| **Embedding** | transformers, sentence-transformers, torch | AI 嵌入模型 |
| **截图** | mss, Pillow | 屏幕截图处理 |
| **输入** | pynput | 全局热键监听 |
| **异步** | celery, asyncio | 异步任务处理 |
| **API** | openai, requests | AI 接口调用 |
| **工具** | psutil, python-dotenv, python-dateutil | 系统工具 |

---

## 配置脚本

我们提供了 2 个配置脚本：

| 脚本名称 | 适用平台 | 环境管理 |
|---------|---------|---------|
| `setup_venv_unix.sh` | macOS / Linux | venv |
| `setup_conda_unix.sh` | macOS / Linux | Conda |

> **Windows 用户**: Windows 脚本暂不可用，请使用手动配置或 WSL

---

## 选择指南

**venv（推荐大多数用户）：**
- ✅ Python 标准库自带，无需额外安装
- ✅ 轻量级，创建速度快
- ✅ 适合纯 Python 项目

**Conda（适合以下情况）：**
- ✅ 需要管理非 Python 依赖（如 CUDA、MKL 等）
- ✅ 需要使用 Conda 特有的包
- ✅ 已经在使用 Anaconda/Miniconda 生态

---

## macOS / Linux 配置

### 使用 venv（推荐）

```bash
# 1. 进入项目目录
cd /path/to/Glimpse

# 2. 给脚本执行权限
chmod +x setup_venv_unix.sh

# 3. 运行配置脚本
./setup_venv_unix.sh
```

### 使用 Conda

```bash
# 1. 确保已安装 Conda
# https://docs.conda.io/en/latest/miniconda.html

# 2. 进入项目目录
cd /path/to/Glimpse

# 3. 给脚本执行权限
chmod +x setup_conda_unix.sh

# 4. 运行配置脚本
./setup_conda_unix.sh
```

---

## Windows 配置

### 方法一：使用 WSL（推荐）

```bash
# 在 WSL 终端中
cd /mnt/d/ISI/Glimpse
chmod +x setup_venv_unix.sh
./setup_venv_unix.sh
```

### 方法二：手动配置

```powershell
# 1. 进入项目目录
cd D:\ISI\Glimpse

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 4. 升级 pip
pip install --upgrade pip setuptools wheel -i https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 6. 配置环境变量
copy .env.example .env
# 编辑 .env 填入你的 API Key
```

---

## 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：

```bash
# API 配置
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
```

---

## 安装后使用

### 激活环境

**macOS / Linux (venv):**
```bash
source venv/bin/activate
```

**macOS / Linux (Conda):**
```bash
conda activate glimpse
```

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

### 运行应用

```bash
python main.py
```

---

## 依赖管理

### 导出当前环境的依赖

```bash
pip freeze > requirements.txt
```

### 使用清华镜像加速

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 故障排除

### Python 版本过低

```bash
# macOS (Homebrew)
brew install python@3.10

# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-pip

# Windows: https://www.python.org/downloads/
```

### SSL 证书错误 (macOS)

```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

### 权限错误

```bash
chmod +x setup_venv_unix.sh
chmod +x setup_conda_unix.sh
```

---

## 获取帮助

- 项目文档: [README.md](README.md)
- 日志文件: `data/glimpse.log`

---

**祝使用愉快！**
