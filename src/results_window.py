from PyQt5.QtGui import QBrush, QFont, QPalette, QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget


class ResultsWindow(QMainWindow):
    def __init__(
        self,
        student_name,
        student_surname,
        student_group,
        elapsed_time,
        startDateTime,
        endDateTime,
    ):
        super().__init__()
        self.student_name = student_name
        self.student_surname = student_surname
        self.student_group = student_group
        self.elapsed_time = elapsed_time
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Итоги")
        self.setGeometry(300, 300, 600, 400)

        # Создание объекта QPixmap с указанным путем к изображению
        pixmap = QPixmap("src/resources/mai2.png")

        # Проверка на успешную загрузку изображения
        if pixmap.isNull():
            print("Ошибка загрузки изображения: убедитесь, что путь к файлу верный")
        else:
            # Установка изображения в качестве фона
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(pixmap))
            self.setPalette(palette)

        central_widget = QWidget(self)  # Создание центрального виджета
        layout = QVBoxLayout(central_widget)  # Создание QVBoxLayout

        font = QFont("Gill Sans", 20)  # Выберите нужный шрифт и размер
        font.setBold(True)  # Делаем текст жирным

        start_time_str = self.startDateTime.toString("dd.MM.yyyy hh:mm:ss")
        end_time_str = self.endDateTime.toString("dd.MM.yyyy hh:mm:ss")

        # Добавляем метки с информацией
        name_label = QLabel(f"Имя: {self.student_name}", self)
        surname_label = QLabel(f"Фамилия: {self.student_surname}", self)
        group_label = QLabel(f"Группа: {self.student_group}", self)
        time_label = QLabel(
            f"Затраченное время: {self.elapsed_time // 60000} мин {self.elapsed_time % 60000 // 1000} сек",
            self,
        )

        # Добавляем метки в макет
        layout.addWidget(name_label)
        layout.addWidget(surname_label)
        layout.addWidget(group_label)
        layout.addWidget(time_label)

        self.setCentralWidget(
            central_widget
        )  # Устанавливаем центральный виджет для QMainWindow
        self.show()  # Показать окно
