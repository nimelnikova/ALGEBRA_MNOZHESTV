import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QInputDialog


def on_check_identity(tableWidget, pair, answer, yes_button, no_button, result_label):
    col1, col2 = pair
    is_identical = True
    non_identical_rows = []  # Индексы строк, где найдены несоответствия

    for row in range(tableWidget.rowCount()):
        item1 = tableWidget.item(row, col1)
        item2 = tableWidget.item(row, col2)
        if item1 and item2 and item1.text() != item2.text():
            is_identical = False
            non_identical_rows.append(row)  # Добавляем номер строки в список

    if (is_identical and answer == "yes") or (not is_identical and answer == "no"):
        if not is_identical and answer == "no":
            row_number, okPressed = QInputDialog.getInt(
                yes_button,
                "Контр-пример",
                "Приведите контр-пример (номер строки в в таблице; первая строка-верхняя):",
                min=1,
                max=tableWidget.rowCount(),
                step=1,
            )
            if okPressed:
                if (
                    row_number - 1
                ) in non_identical_rows:  # Проверяем, входит ли номер строки в список несоответствий
                    result_label.setText("Контр-пример верен!")
                    result_label.setStyleSheet("background-color: lightgreen;")
                else:
                    result_label.setText("Неверный контр-пример. Начните заново")
                    result_label.setStyleSheet("background-color: salmon;")
                    sys.exit(1)
        else:
            result_label.setText("Ваш ответ верен!")
            result_label.setStyleSheet("background-color: lightgreen;")
    else:
        result_label.setText("Ваш ответ неверен. Начните заново")
        result_label.setStyleSheet("background-color: salmon;")
        sys.exit(1)


def setup_identity_check(window, tableWidget, pairs):
    for index, (col1, col2) in enumerate(pairs):
        formula_label = QLabel(
            f"Верно ли тождество? {window.expressions[col1 - 3]} ≡ {window.expressions[col2 - 3]}",
            window,
        )
        font = QFont("Copperplate", 21)

        formula_label.setFont(font)
        formula_label.setAlignment(Qt.AlignCenter)

        yes_button = QPushButton("Да", window)
        yes_button.setFont(font)
        no_button = QPushButton("Нет", window)
        no_button.setFont(font)
        result_label = QLabel("Ожидание ответа...", window)
        result_label.setFont(font)
        result_label.setAlignment(Qt.AlignCenter)

        yes_button.setObjectName(f"yesButton_{index}")
        no_button.setObjectName(f"noButton_{index}")

        yes_button.clicked.connect(
            lambda _, b=yes_button, nb=no_button, p=(
                col1,
                col2,
            ), rl=result_label: on_check_identity(tableWidget, p, "yes", b, nb, rl)
        )
        no_button.clicked.connect(
            lambda _, b=no_button, nb=yes_button, p=(
                col1,
                col2,
            ), rl=result_label: on_check_identity(tableWidget, p, "no", b, nb, rl)
        )

        identity_layout = QHBoxLayout()
        identity_layout.addWidget(formula_label)
        identity_layout.addWidget(yes_button)
        identity_layout.addWidget(no_button)
        identity_layout.addWidget(result_label)
        identity_layout.addStretch()

        window.inner_layout.addStretch(1)
        window.inner_layout.addLayout(identity_layout)
