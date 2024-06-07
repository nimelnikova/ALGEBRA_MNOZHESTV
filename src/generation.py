# Стандартные библиотеки
import random
import sys
from itertools import product

# Сторонние библиотеки
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

# Модули текущего проекта
from src.check import check_truth_table
from src.identity import setup_identity_check
from src.results_window import ResultsWindow


# Список всех возможных выражений
all_expressions = [
    "(A ∩ B) ∪ C",  # 1 вариант
    "A + (B ∩ C)",  # 1 вариант
    "(C ∩ ¬B) + (A + C)",  # 1 вариант
    "((A \\ B) \\ C) + (A \\ C)",  # 2 вариант
    "B \\ (C ∪ ¬A)",  # 2 вариант
    "(A \\ B) \\ C",  # 2 вариант
    "(¬A ∩ ¬B) ∪ ¬C + (¬A + (¬B ∪ C))",  # 3 вариант
    "((A ∪ B) ∩ C) + A + (¬B ∪ C)",  # 3 вариант
    "¬B + ((B ∪ ¬C) ∩ A)",  # 3 вариант
    "C \\ (B ∪ ¬A)",  # 4 вариант
    "A \\ (B ∪ ¬C)",  # 4 вариант
    "(A + ¬C) ∩ (¬B + ¬A)",  # 4 вариант
    "(A ∩ C) \\ (C ∩ ¬B)",  # 5 вариант
    "C \\ (B ∪ ¬A)",  # 5 вариант
    "(C \\ B) + (C \\ (B \\ A))",  # 5 вариант
    "A + C + (A ∪ B)",  # 6 вариант
    "B \\ (C ∩ ¬A)",  # 6 вариант
    "C + (B \\ A)",  # 6 вариант
    "A ∪ ¬B ∪ (C ∪ ¬A)",  # 7 вариант
    "((A ∪ C) ∩ A) + (¬B ∪ C)",  # 7 вариант
    "A + ((¬B ∪ C) ∩ ¬A) ∪ B",  # 7 вариант
    "(A \\ B) + (A \\ C)",  # 8 вариант
    "(B + C) ∩ A",  # 8 вариант
    "C + (B \\ ¬A)",  # 8 вариант
    "A ∩ (¬B ∪ ¬C) ∩ C",  # 9 вариант
    "(A ∪ B) ∩ ¬C + ¬A + (¬B ∪ C)",  # 9 вариант
    "A ∩ ¬B ∩ (C + B)",  # 9 вариант
    "((A ∪ B) ∩ C) + (¬A ∩ ¬B)",  # 10 вариант
    "A + ¬B ∪ (C ∩ ¬B ∪ C)",  # 10 вариант
    "((A ∪ B) ∪ (¬A ∩ C)) + ¬C",  # 10 вариант
]


# Функция для случайного выбора варианта выражений
def get_random_expressions():
    variant_number = random.randint(
        1, 10
    )  # Выбираем случайный номер варианта от 1 до 10
    start_index = (variant_number - 1) * 3
    return all_expressions[start_index : start_index + 3]


class MainWindow(QMainWindow):
    def __init__(
        self,
        student_name="",
        student_surname="",
        student_group="",
        timer=None,
        startDateTime=None,
    ):
        super().__init__()
        self.student_name = student_name
        self.student_surname = student_surname
        self.student_group = student_group
        self.timer = timer
        self.startDateTime = startDateTime
        self.title = "Алгебра множеств"
        self.width = 1030
        self.height = 1028
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background: transparent;")

        self.background_label = QLabel(self.central_widget)
        self.background_label.setGeometry(0, 0, self.width, self.height)
        self.pixmap = QPixmap("src/resources/mai2.png")
        if not self.pixmap.isNull():
            self.background_label.setPixmap(
                self.pixmap.scaled(
                    self.width, self.height, Qt.KeepAspectRatioByExpanding
                )
            )

        self.font = QFont("Copperplate", 24)
        self.inner_layout = QVBoxLayout(self.central_widget)
        self.inner_layout.setSpacing(5)

        self.generate_table_and_expressions()
        self.setup_buttons_and_labels()

    def generate_table_and_expressions(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setFont(self.font)
        self.expressions = get_random_expressions()
        column_titles = ["A", "B", "C"] + self.expressions
        self.tableWidget.setColumnCount(len(column_titles))
        self.tableWidget.setRowCount(8)
        self.tableWidget.setHorizontalHeaderLabels(column_titles)
        self.tableWidget.horizontalHeader().setFont(self.font)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tableWidget.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(row, 30)

        truth_table = list(product([0, 1], repeat=3))
        for row_num, (a, b, c) in enumerate(truth_table):
            for j in range(3):
                self.tableWidget.setItem(
                    row_num, j, QTableWidgetItem(str(truth_table[row_num][j]))
                )
            for j in range(3, 6):
                self.tableWidget.setItem(row_num, j, QTableWidgetItem(""))

        # Установка белого контура
        self.tableWidget.setStyleSheet(
            """
            QTableWidget {
                background-color: transparent;
                color: white;  
            }
            QTableWidget::item {
                border-bottom: 1px solid white;
                border-right: 1px solid white;
            }
            QHeaderView::section {
                background-color: transparent;
                border: 2px solid white;
            }
        """
        )

        table_height = (
            self.tableWidget.horizontalHeader().height()
            + self.tableWidget.rowHeight(0) * self.tableWidget.rowCount()
        )
        self.tableWidget.setFixedHeight(table_height)
        self.inner_layout.addWidget(self.tableWidget)

    def setup_buttons_and_labels(self):
        # Создаем кнопку и устанавливаем ее шрифт

        self.check_button = QPushButton("Проверить таблицу")
        self.check_button.setFont(self.font)
        self.check_button.setFixedHeight(50)

        # Подключаем событие нажатия на кнопку
        self.check_button.clicked.connect(
            lambda: check_truth_table(self, self.expressions, self.tableWidget)
        )

        # Добавляем кнопку в вертикальный макет под таблицей
        self.inner_layout.addWidget(self.check_button)

        # Настройка проверки тождественности
        pairs = [(3, 4), (4, 5), (3, 5)]
        setup_identity_check(self, self.tableWidget, pairs)

        # Кнопка для завершения выполнения
        self.finish_button = QPushButton("Завершить выполнение", self)
        self.finish_button.setFont(self.font)
        self.finish_button.setFixedHeight(50)
        self.finish_button.clicked.connect(self.finish_assignment)

        # Добавляем кнопку в вертикальный макет под таблицей
        self.inner_layout.addWidget(self.finish_button)
        self.inner_layout.setSpacing(1)

    def finish_assignment(self):
        # Зафиксировать время завершения
        self.endDateTime = QDateTime.currentDateTime()

        # Вычислить затраченное время
        elapsed_time = self.timer.elapsed()

        # Собрать данные студента
        student_name = self.student_name
        student_surname = self.student_surname
        student_group = self.student_group

        # Форматировать строки начала и завершения для вывода
        start_time_str = self.startDateTime.toString("dd.MM.yyyy hh:mm:ss")
        end_time_str = self.endDateTime.toString("dd.MM.yyyy hh:mm:ss")

        # Создать экземпляр ResultsWindow с необходимыми параметрами
        self.results_window = ResultsWindow(
            student_name,
            student_surname,
            student_group,
            elapsed_time,
            self.startDateTime,
            self.endDateTime,
        )
        self.results_window.show()

        # Вывести информационное сообщение
        QMessageBox.information(
            self,
            "Информация о студенте",
            f"ФИО: {student_surname} {student_name}\n"
            f"Группа: {student_group}\n"
            f"Начало выполнения: {start_time_str}\n"
            f"Окончание выполнения: {end_time_str}\n"
            f"Продолжительность выполнения: {elapsed_time // 60000} мин {elapsed_time % 60000 // 1000} сек",
            QMessageBox.Ok,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
