# Стандартные библиотеки
import sys

# Сторонние библиотеки
from PyQt5.QtCore import (
    QPoint,
    QPropertyAnimation,
    Qt,
    QDateTime,
    QEasingCurve,
    QTime,
    pyqtProperty,
)
from PyQt5.QtGui import QBrush, QColor, QFont, QPalette, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QFrame,
    QGraphicsDropShadowEffect,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Модули текущего проекта
from src.generation import MainWindow


class AnimatedLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation = None

    def get_pos(self):
        return super().pos()

    def set_pos(self, pos):
        self.move(pos)

    pos = pyqtProperty(QPoint, get_pos, set_pos)


class CustomLineEdit(QLineEdit):
    def __init__(self, label_text, parent=None):
        super().__init__(parent)
        self.label = AnimatedLabel(self)
        self.label.setText(label_text)
        self.label.setStyleSheet("color: #a1a1a1;")
        self.label.adjustSize()
        self.label.move(
            10, self.height() - self.label.height()
        )  # Initial label position
        self.textChanged.connect(self.handle_text_changed)
        self.focused = False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.focused or not self.text():
            self.label.move(10, int(self.height() / 2 - self.label.height() / 2))

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused = True
        self.animate_label()

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.text():
            self.focused = False
            self.animate_label()

    def animate_label(self):
        if self.focused and self.text():
            end_pos = QPoint(10, -15)
        else:
            end_pos = QPoint(10, int(self.height() / 2 - self.label.height() / 2))

        self.animation = QPropertyAnimation(self.label, b"pos")
        self.animation.setDuration(200)
        self.animation.setEndValue(end_pos)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        self.animation.start()
        self.label.raise_()

    def handle_text_changed(self, text):
        self.focused = bool(text)
        self.animate_label()


class HighlightableFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setMouseTracking(True)  # Enable mouse tracking

    def initUI(self):
        self.setStyleSheet(
            """
            background-color: rgba(255, 255, 255, 250);
            border-radius: 20px;
        """
        )
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(300)
        self.shadowEffect.setOffset(0)
        self.setGraphicsEffect(self.shadowEffect)

    def enterEvent(self, event):
        # Инициализация эффекта тени с базовыми параметрами при входе курсора
        self.initShadowEffect()

    def initShadowEffect(self):
        # Базовая инициализация эффекта тени
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(400)
        self.shadowEffect.setOffset(0)
        self.setGraphicsEffect(self.shadowEffect)

    def leaveEvent(self, event):
        # Сделать тень невидимой при выходе курсора
        self.shadowEffect.setColor(QColor(0, 0, 0, 0))

    def mouseMoveEvent(self, event):
        x = event.pos().x()
        width = self.width()
        # Рассчитать оттенок серого в зависимости от положения курсора
        gradient_ratio = x / width
        color_value = int(255 * gradient_ratio)  # От 0 (черный) до 255 (белый)
        self.shadowEffect.setColor(QColor(color_value, color_value, color_value))

    def updateShadowColor(self, color):
        self.shadowEffect.setColor(color)
        self.setGraphicsEffect(self.shadowEffect)


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # Инициализация и запуск таймера
        self.timer = QTime()
        self.startButton.clicked.connect(self.openTruthTableWindow)

    def initUI(self):
        palette = QPalette()
        pixmap = QPixmap("src/resources/mai1.png")  # Указываем имя файла в текущей дир
        if pixmap.isNull():
            print("Ошибка загрузки изображения: убедитесь, что файл доступен")
        else:
            # Масштабируем изображение, чтобы оно соответствовало размеру окна
            scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
            palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
            self.setPalette(palette)

        backgroundFrame = HighlightableFrame(self)
        backgroundFrame.setFixedSize(425, 335)

        lineEditStyle = """
        QLineEdit {
            color: #000;
            border: none;
            border-bottom: 1px solid #000;
            font-size: 20px;
            background: transparent;
        }
        """

        self.nameEdit = CustomLineEdit("Введите имя, пожалуйста")
        self.nameEdit.setStyleSheet(lineEditStyle)
        self.surnameEdit = CustomLineEdit("Фамилия")
        self.surnameEdit.setStyleSheet(lineEditStyle)
        self.groupEdit = CustomLineEdit("Номер группы")
        self.groupEdit.setStyleSheet(lineEditStyle)

        self.startButton = QPushButton("нажмите для старта!")
        self.startButton.setStyleSheet(
            """
            QPushButton {
                background-color: #00b4d8;
                border-radius: 15px;
                padding: 20px 35px;
                font-size: 20px;
                color: white;
            }
            QPushButton:hover {
                background-color: #0096c7;
            }
        """
        )

        aptosFont = QFont("Gill Sans", 22)
        self.nameEdit.setFont(aptosFont)
        self.surnameEdit.setFont(aptosFont)
        self.groupEdit.setFont(aptosFont)
        self.startButton.setFont(aptosFont)

        formLayout = QVBoxLayout()
        formLayout.addWidget(self.nameEdit)
        formLayout.addWidget(self.surnameEdit)
        formLayout.addWidget(self.groupEdit)
        formLayout.addWidget(self.startButton)
        formLayout.setSpacing(15)
        formLayout.setContentsMargins(50, 40, 50, 40)

        backgroundFrame.setLayout(formLayout)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(backgroundFrame, 0, Qt.AlignCenter)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(mainLayout)
        self.setFixedSize(630, 650)
        self.setWindowTitle("Добро пожаловать!")

    def openTruthTableWindow(self):
        self.startDateTime = QDateTime.currentDateTime()
        self.timer.start()
        # Считываем данные из полей ввода
        name = self.nameEdit.text()
        surname = self.surnameEdit.text()
        group = self.groupEdit.text()

        self.truth_table_window = MainWindow(
            name, surname, group, self.timer, self.startDateTime
        )
        self.truth_table_window.show()
        self.hide()  # Скрываем текущее окно


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = WelcomeWindow()
    ex.show()
    sys.exit(app.exec_())
