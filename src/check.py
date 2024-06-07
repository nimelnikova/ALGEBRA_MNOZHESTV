import sys
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QColor, QBrush


def evaluate_expression(expression, a, b, c):
    # Преобразуем логические значения в числа для выполнения операций
    expression = (
        expression.replace("¬A", "int(not a)")
        .replace("¬B", "int(not b)")
        .replace("¬C", "int(not c)")
        .replace("A", str(int(a)))
        .replace("B", str(int(b)))
        .replace("C", str(int(c)))
        .replace("∩", " and ")
        .replace("∪", " or ")
        .replace("\\", " and not ")
        .replace("+", " ^ ")
    )
    return eval(expression)


def check_truth_table(window, expressions, tableWidget):
    truth_table = [
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 1),
    ]
    all_correct = True
    for i, (a, b, c) in enumerate(truth_table):
        for j, expression in enumerate(expressions):
            expected_value = evaluate_expression(expression, a, b, c)
            item = tableWidget.item(i, j + 3)
            if item is None:
                item = (
                    QTableWidgetItem()
                )  # Создаем новый элемент, если его не существует
                tableWidget.setItem(i, j + 3, item)
            user_input = item.text()
            correct = user_input.isdigit() and int(user_input) == expected_value
            if not correct:
                item.setBackground(QBrush(QColor(255, 0, 0)))  # Красный
                all_correct = False
            else:
                item.setBackground(QBrush(QColor(0, 255, 0)))  # Зелёный

    tableWidget.viewport().update()

    if all_correct:
        QMessageBox.information(
            window,
            "Проверка",
            "Все ответы верные! Продолжайте выполнять задание",
        )
    else:
        QMessageBox.warning(
            window, "Проверка", "Некоторые ответы неверные. Начните заново."
        )
        sys.exit(1)
