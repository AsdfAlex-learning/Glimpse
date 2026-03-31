"""
UI 样式定义
支持浅色/深色/跟随系统模式
"""

# ===== 浅色主题 =====
LIGHT_THEME = {
    "name": "light",
    "background": "#ffffff",
    "surface": "#fafafa",
    "card": "#ffffff",
    "border": "#e0e0e0",
    "text": "#212121",
    "text_secondary": "#757575",
    "accent": "#4CAF50",
    "accent_hover": "#45a049",
    "error": "#f44336",
    "warning": "#ff9800",
    "info": "#2196F3",
}

# ===== 深色主题 =====
DARK_THEME = {
    "name": "dark",
    "background": "#121212",
    "surface": "#1e1e1e",
    "card": "#252525",
    "border": "#333333",
    "text": "#ffffff",
    "text_secondary": "#b0b0b0",
    "accent": "#66bb6a",
    "accent_hover": "#81c784",
    "error": "#ef5350",
    "warning": "#ffa726",
    "info": "#42a5f5",
}


def get_stylesheet(theme: dict) -> str:
    """
    生成 QSS 样式表

    Args:
        theme: 主题字典

    Returns:
        QSS 样式表字符串
    """
    return f"""
    /* ===== 全局样式 ===== */
    QWidget {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 14px;
        color: {theme["text"]};
        background-color: {theme["background"]};
    }}

    /* ===== 主窗口 ===== */
    QMainWindow {{
        background-color: {theme["background"]};
    }}

    /* ===== 按钮 ===== */
    QPushButton {{
        background-color: {theme["accent"]};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background-color: {theme["accent_hover"]};
    }}

    QPushButton:pressed {{
        background-color: {theme["accent"]};
    }}

    QPushButton:disabled {{
        background-color: {theme["border"]};
        color: {theme["text_secondary"]};
    }}

    /* ===== 次要按钮 ===== */
    QPushButton.secondary {{
        background-color: {theme["surface"]};
        color: {theme["text"]};
        border: 1px solid {theme["border"]};
    }}

    QPushButton.secondary:hover {{
        background-color: {theme["border"]};
    }}

    /* ===== 输入框 ===== */
    QLineEdit {{
        background-color: {theme["card"]};
        border: 2px solid {theme["border"]};
        border-radius: 6px;
        padding: 8px 12px;
        color: {theme["text"]};
    }}

    QLineEdit:focus {{
        border-color: {theme["accent"]};
    }}

    QLineEdit:disabled {{
        background-color: {theme["surface"]};
        color: {theme["text_secondary"]};
    }}

    /* ===== 文本编辑框 ===== */
    QTextEdit {{
        background-color: {theme["card"]};
        border: 1px solid {theme["border"]};
        border-radius: 6px;
        padding: 12px;
        color: {theme["text"]};
    }}

    QTextEdit:focus {{
        border-color: {theme["accent"]};
    }}

    /* ===== 列表 ===== */
    QListWidget {{
        background-color: {theme["surface"]};
        border: none;
        border-radius: 8px;
        padding: 8px;
        outline: none;
    }}

    QListWidget::item {{
        background-color: {theme["card"]};
        border-radius: 8px;
        padding: 12px;
        margin: 4px 0px;
        border: 2px solid transparent;
    }}

    QListWidget::item:hover {{
        background-color: {theme["surface"]};
        border-color: {theme["border"]};
    }}

    QListWidget::item:selected {{
        background-color: {theme["accent"]} + "20";
        border-color: {theme["accent"]};
    }}

    /* ===== 滚动条 ===== */
    QScrollBar:vertical {{
        background-color: {theme["surface"]};
        width: 12px;
        border-radius: 6px;
    }}

    QScrollBar::handle:vertical {{
        background-color: {theme["border"]};
        border-radius: 6px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {theme["text_secondary"]};
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    /* ===== 标签 ===== */
    QLabel {{
        color: {theme["text"]};
    }}

    QLabel.secondary {{
        color: {theme["text_secondary"]};
        font-size: 12px;
    }}

    /* ===== 分割线 ===== */
    QFrame[frameShape="4"] {{  # HLine
        color: {theme["border"]};
    }}

    /* ===== 工具提示 ===== */
    QToolTip {{
        background-color: {theme["card"]};
        color: {theme["text"]};
        border: 1px solid {theme["border"]};
        border-radius: 4px;
        padding: 4px 8px;
    }}
"""


def get_current_theme() -> dict:
    """
    获取当前主题

    Returns:
        主题字典
    """
    from app.core.settings import settings_manager

    settings = settings_manager.get_settings()
    theme_setting = settings.theme  # "light", "dark", "system"

    if theme_setting == "system":
        from app.utils.helpers import get_system_theme
        system_theme = get_system_theme()
        return DARK_THEME if system_theme == "dark" else LIGHT_THEME

    return DARK_THEME if theme_setting == "dark" else LIGHT_THEME


def apply_theme(widget, theme: dict = None):
    """
    应用主题到部件

    Args:
        widget: 要应用主题的部件
        theme: 主题字典，None 则使用当前主题
    """
    if theme is None:
        theme = get_current_theme()

    stylesheet = get_stylesheet(theme)
    widget.setStyleSheet(stylesheet)
