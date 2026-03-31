"""
区域选择器模块

提供屏幕区域选择功能，支持鼠标拖拽选择区域。
"""
import sys
from typing import Optional, Tuple, Callable
from PySide6.QtWidgets import (
    QApplication, QWidget, QRubberBand, QLabel
)
from PySide6.QtCore import Qt, QRect, QPoint, Signal, Slot
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QScreen

from app.core.logger import Logger

logger = Logger.get_logger()


class RegionSelector(QWidget):
    """
    区域选择器窗口

    全屏半透明遮罩，支持鼠标拖拽选择区域。

    Signals:
        region_selected: 当用户确认选择区域时发射，参数为 (x, y, width, height)
        selection_cancelled: 当用户取消选择时发射
    """

    region_selected = Signal(int, int, int, int)  # x, y, width, height
    selection_cancelled = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setWindowTitle("区域截图 - 拖拽选择区域，Enter确认，Esc取消")

        # 设置窗口属性
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 获取主屏幕并设置全屏
        screen = QApplication.primaryScreen()
        if screen:
            self.setGeometry(screen.geometry())
        else:
            self.showFullScreen()

        # 选择相关变量
        self._rubber_band: Optional[QRubberBand] = None
        self._start_pos: Optional[QPoint] = None
        self._current_rect: Optional[QRect] = None
        self._is_selecting = False

        # 创建提示标签
        self._create_hint_label()

        logger.info("区域选择器初始化完成")

    def _create_hint_label(self):
        """创建操作提示标签"""
        self._hint_label = QLabel(self)
        self._hint_label.setText(
            "🖱️ 拖拽鼠标选择区域\n"
            "✅ Enter 或双击确认\n"
            "❌ Esc 取消"
        )
        self._hint_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                padding: 15px;
                border-radius: 10px;
                font-size: 14px;
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
        """)
        self._hint_label.adjustSize()

        # 居中显示
        screen = QApplication.primaryScreen()
        if screen:
            center = screen.geometry().center()
            label_rect = self._hint_label.geometry()
            label_rect.moveCenter(center)
            self._hint_label.move(label_rect.topLeft())

    def paintEvent(self, event):
        """绘制半透明遮罩"""
        painter = QPainter(self)

        # 绘制半透明黑色遮罩
        overlay_color = QColor(0, 0, 0, 80)  # ARGB，80/255 透明度
        painter.fillRect(self.rect(), overlay_color)

        # 如果有选择区域，绘制高亮边框
        if self._current_rect and self._current_rect.isValid():
            # 清除选择区域的遮罩（绘制透明矩形）
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(self._current_rect, Qt.GlobalColor.transparent)

            # 绘制选择区域边框
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            pen = QPen(QColor(0, 150, 255), 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)
            painter.drawRect(self._current_rect)

            # 绘制尺寸信息
            self._draw_size_info(painter, self._current_rect)

        painter.end()

    def _draw_size_info(self, painter: QPainter, rect: QRect):
        """在选择区域旁边绘制尺寸信息"""
        width = rect.width()
        height = rect.height()

        text = f"{width} x {height}"

        # 计算文本位置（在矩形下方或上方）
        font = QFont('Microsoft YaHei', 10)
        painter.setFont(font)

        text_rect = painter.boundingRect(rect, Qt.TextFlag.TextSingleLine, text)

        # 如果矩形太靠近底部，则在上方显示
        if rect.bottom() + text_rect.height() + 5 > self.height():
            text_rect.moveBottomLeft(rect.topLeft() - QPoint(0, 5))
        else:
            text_rect.moveTopLeft(rect.bottomLeft() + QPoint(0, 5))

        # 绘制背景
        bg_color = QColor(0, 0, 0, 160)
        painter.fillRect(text_rect.adjusted(-4, -2, 4, 2), bg_color)

        # 绘制文本
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_pos = event.pos()
            self._is_selecting = True

            # 隐藏提示标签
            self._hint_label.hide()

            # 创建橡皮筋选择框
            if self._rubber_band is None:
                self._rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
                self._rubber_band.setStyleSheet("""
                    QRubberBand {
                        border: 2px solid #0096FF;
                        background-color: rgba(0, 150, 255, 30);
                    }
                """)

            self._rubber_band.setGeometry(QRect(self._start_pos, QSize()))
            self._rubber_band.show()

            logger.debug(f"开始选择区域: {self._start_pos}")

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self._is_selecting and self._start_pos:
            end_pos = event.pos()
            rect = QRect(self._start_pos, end_pos).normalized()

            # 限制在窗口范围内
            rect = rect.intersected(self.rect())

            self._current_rect = rect

            if self._rubber_band:
                self._rubber_band.setGeometry(rect)

            # 触发重绘以更新遮罩和尺寸信息
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton and self._is_selecting:
            self._is_selecting = False

            if self._current_rect and self._current_rect.isValid():
                size = self._current_rect.size()
                if size.width() > 10 and size.height() > 10:
                    logger.info(f"选择区域: {self._current_rect}")
                else:
                    logger.warning("选择的区域太小，已忽略")
                    self._reset_selection()
            else:
                self._reset_selection()

    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件 - 确认选择"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self._current_rect and self._current_rect.isValid():
                self._confirm_selection()

    def keyPressEvent(self, event):
        """键盘事件"""
        key = event.key()

        if key == Qt.Key.Key_Escape:
            # 取消选择
            logger.info("用户取消区域选择")
            self._reset_selection()
            self.selection_cancelled.emit()
            self.close()

        elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            # 确认选择
            if self._current_rect and self._current_rect.isValid():
                self._confirm_selection()
            else:
                logger.warning("没有有效的选择区域，无法确认")

    def _confirm_selection(self):
        """确认选择并发射信号"""
        if self._current_rect:
            rect = self._current_rect
            logger.info(f"确认选择区域: ({rect.x()}, {rect.y()}, {rect.width()}, {rect.height()})")
            self.region_selected.emit(rect.x(), rect.y(), rect.width(), rect.height())
            self.close()

    def _reset_selection(self):
        """重置选择状态"""
        self._start_pos = None
        self._current_rect = None
        self._is_selecting = False

        if self._rubber_band:
            self._rubber_band.hide()

        self.update()

        # 重新显示提示
        self._hint_label.show()

    def showEvent(self, event):
        """显示事件"""
        super().showEvent(event)
        logger.info("区域选择器已显示")

        # 确保提示标签在最上层
        self._hint_label.raise_()

    def closeEvent(self, event):
        """关闭事件"""
        logger.info("区域选择器关闭")
        super().closeEvent(event)


def select_region(
    on_selected: Optional[Callable[[int, int, int, int], None]] = None,
    on_cancelled: Optional[Callable[[], None]] = None
) -> Optional[Tuple[int, int, int, int]]:
    """
    同步方式选择屏幕区域

    注意：这会阻塞当前线程，直到用户完成选择或取消。
    在非 GUI 线程中调用时需要注意。

    Args:
        on_selected: 选择完成时的回调函数，参数为 (x, y, width, height)
        on_cancelled: 取消选择时的回调函数

    Returns:
        如果用户选择了区域，返回 (x, y, width, height)
        如果用户取消或出错，返回 None
    """
    # 检查是否有 QApplication 实例
    app = QApplication.instance()
    created_app = False

    if not app:
        app = QApplication(sys.argv)
        created_app = True

    result = {'rect': None, 'cancelled': False}

    def on_region_selected(x, y, w, h):
        result['rect'] = (x, y, w, h)
        if on_selected:
            on_selected(x, y, w, h)

    def on_selection_cancelled():
        result['cancelled'] = True
        if on_cancelled:
            on_cancelled()

    selector = RegionSelector()
    selector.region_selected.connect(on_region_selected)
    selector.selection_cancelled.connect(on_selection_cancelled)

    selector.show()

    if created_app:
        app.exec()
    else:
        # 等待选择器关闭
        loop = 0
        while selector.isVisible() and loop < 3000:  # 最多等待 5 分钟
            QApplication.processEvents()
            time.sleep(0.1)
            loop += 1

    return result['rect']


# 便捷函数

def grab_region(x: int, y: int, width: int, height: int) -> 'PIL.Image.Image':
    """
    截取指定区域的屏幕图像

    Args:
        x: 左上角 X 坐标
        y: 左上角 Y 坐标
        width: 区域宽度
        height: 区域高度

    Returns:
        PIL Image 对象
    """
    import mss
    from PIL import Image

    with mss.mss() as sct:
        monitor = {"left": x, "top": y, "width": width, "height": height}
        screenshot = sct.grab(monitor)
        return Image.frombytes("RGB", screenshot.size, screenshot.rgb)


if __name__ == "__main__":
    # 测试代码
    print("Testing RegionSelector...")

    result = select_region()

    if result:
        x, y, w, h = result
        print(f"Selected region: ({x}, {y}, {w}, {h})")

        # 测试截图
        img = grab_region(x, y, w, h)
        img.save("test_region.png")
        print("Screenshot saved to test_region.png")
    else:
        print("Selection cancelled")