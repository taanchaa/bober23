"""
 Модуль содержит реализацию класса управления приложением через графический интерфейс
"""
import sys
from data import Controls
from PySide6.QtCore import QCoreApplication
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6 import QtWidgets
from bookkeepersq3.view.ui_new_operation import Ui_Dialog
from bookkeepersq3.view.ui_set_budget import Ui_Dialog_set_budget
from bookkeepersq3.view.ui_new_category import Ui_Dialog_new_category
from bookkeepersq3.view.ui_exception import Ui_Dialog_exception
from bookkeepersq3.view.ui_main import Ui_MainWindow


class ExpanseTracer(QMainWindow):
    """
    Класс содержит методы реализующие управление приложением
    через графический интерфейс
    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn = Controls()
        self.view_data()
        self.ui.pushButton_4.clicked.connect(self.open_new_transaction_window)
        self.ui.pushButton_5.clicked.connect(self.open_new_transaction_window)
        self.ui.pushButton_6.clicked.connect(self.delete_current_transaction)
        self.ui.pushButton.clicked.connect(self.open_new_set_budget_window)
        self.ui.pushButton_2.clicked.connect(self.open_new_category_window)
        self.ui.pushButton_3.clicked.connect(self.open_new_category_window)
        self.ui.pushButton_7.clicked.connect(self.delete_current_category)

    def reload_data(self) -> None:
        """
        Метод для обновления виджетов с данными о расходах за день, неделю, месяц
        """
        self.ui.label_6.setText(self.conn.get_budget_per_day())
        self.ui.label_8.setText(self.conn.get_budget_per_week())
        self.ui.label_10.setText(self.conn.get_budget_per_month())
        self.ui.label_7.setText(self.conn.get_a_budget_limit('LimitPerDay'))
        self.ui.label_9.setText(self.conn.get_a_budget_limit('LimitPerWeek'))
        self.ui.label_11.setText(self.conn.get_a_budget_limit('LimitPerMonth'))

    def view_data(self) -> None:
        """
        Метод для просмотра таблиц с записями о расходах и списком категорий
        """
        self.model = QSqlTableModel(self)
        self.model.setTable('Recent_expenses')
        self.model.select()
        self.ui.tableView.setModel(self.model)
        self.model = QSqlTableModel(self)
        self.model.setTable('Categories_storage')
        self.model.select()
        self.ui.tableView_2.setModel(self.model)

    def open_new_transaction_window(self) -> None:
        """
        Метод открывает диалоговое окно для добавления новой записи о расходах или
        изменения имеющейся
        """
        self.new_window = QtWidgets.QDialog()
        self.ui_window = Ui_Dialog()
        self.ui_window.setupUi(self.new_window)
        self.new_window.show()
        sender = self.sender()
        if (sender.text() ==
                QCoreApplication.translate
                ("MainWindow",
                "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u041e\u043f\u0435\u0440\u0430\u0446\u0438\u044e"
                , None)):
            self.ui_window.pushButton.clicked.connect(self.add_new_transaction)
        else:
            self.ui_window.pushButton.clicked.connect(self.edit_current_transaction)

    def open_new_set_budget_window(self) -> None:
        """
        Метод открывает диалоговое окно для установки ограничений бюджета
        """
        self.new_window_set_budget = QtWidgets.QDialog()
        self.ui_window_set_budget = Ui_Dialog_set_budget()
        self.ui_window_set_budget.setupUi(self.new_window_set_budget)
        self.new_window_set_budget.show()
        self.ui_window_set_budget.pushButton.clicked.connect(self.set_budget)

    def open_new_category_window(self) -> None:
        """
        Метод открывает диалоговое окно для добавления новой категории или
        изменения имеющейся
        """
        self.new_window_category = QtWidgets.QDialog()
        self.ui_window_category = Ui_Dialog_new_category()
        self.ui_window_category.setupUi(self.new_window_category)
        self.new_window_category.show()
        sender = self.sender()
        if (sender.text() ==
            QCoreApplication.translate
            ("MainWindow",
            "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044e"
            , None)):
            self.ui_window_category.pushButton.clicked.connect(self.add_new_category)
        else:
            (self.ui_window_category.pushButton.clicked.connect
             (self.edit_current_category))

    def open_new_exception_window(self, exception_text: str) -> None:
        """
        Метод открывает диалоговое окно для сообщения об ошибке
        """
        self.new_window_exception = QtWidgets.QDialog()
        self.ui_window_exception = Ui_Dialog_exception()
        self.ui_window_exception.setupUi(self.new_window_exception)
        self.ui_window_exception.label_2.setText(exception_text)
        self.new_window_exception.show()

    def add_new_transaction(self) -> None:
        """
        Метод для заполнения информации о новой записи о расходах
        и вызова метода добавления новой записи в базу данных
        """
        index = self.ui.tableView_2.selectedIndexes()[0]
        id_ind = self.ui.tableView_2.model().data(index)
        category = self.conn.get_a_category_by_id(id_ind)
        price = self.ui_window.price.text()
        comment = self.ui_window.comment.text()
        try:
            self.conn.add_a_position(price, category, comment)
        except ValueError:
            self.open_new_exception_window('Графа "Стоимость" должна '
                                           'содержать целое или дробное число')
        finally:
            self.reload_data()
            self.view_data()
            self.new_window.close()

    def add_new_category(self) -> None:
        """
        Метод для заполнения информации о новой категории
        и вызова метода добавления новой категории в базу данных
        """
        category = self.ui_window_category.price.text()
        try:
            self.conn.add_a_category(category)
        except ValueError:
            self.open_new_exception_window("Название категории не "
                                           "должно содержать цифр")
        self.reload_data()
        self.view_data()
        self.new_window_category.close()

    def edit_current_transaction(self) -> None:
        """
        Метод для заполнения информации об измененной записи о расходах
        и вызова метода обновления записи о расходах в базе данных
        """
        index = self.ui.tableView.selectedIndexes()[0]
        id_ind = self.ui.tableView.model().data(index)
        index2 = self.ui.tableView_2.selectedIndexes()[0]
        id2 = self.ui.tableView_2.model().data(index2)
        category = self.conn.get_a_category_by_id(id2)
        price = self.ui_window.price.text()
        comment = self.ui_window.comment.text()
        try:
            self.conn.update_position(id_ind, price, category, comment)
        except ValueError:
            self.open_new_exception_window('Графа "Стоимость" должна содержать'
                                           ' целое или дробное число')
        self.reload_data()
        self.view_data()
        self.new_window.close()

    def edit_current_category(self) -> None:
        """
        Метод для заполнения информации об измененной категории
        и вызова метода обновления категории в базе данных
        """
        index = self.ui.tableView_2.selectedIndexes()[0]
        id_ind = self.ui.tableView_2.model().data(index)
        category = self.ui_window_category.price.text()
        try:
            self.conn.update_category(id_ind, category)
        except ValueError:
            self.open_new_exception_window("Название категории не должно содержать цифр")
        self.reload_data()
        self.view_data()
        self.new_window_category.close()

    def delete_current_transaction(self) -> None:
        """
        Метод для удаления записи о расходах
        """
        index = self.ui.tableView.selectedIndexes()[0]
        id_ind = self.ui.tableView.model().data(index)
        self.conn.delete_a_position_by_id(id_ind)
        self.reload_data()
        self.view_data()

    def delete_current_category(self) -> None:
        """
        Метод для удаления категории
        """
        index = self.ui.tableView_2.selectedIndexes()[0]
        id_ind = self.ui.tableView_2.model().data(index)
        self.conn.delete_a_category_by_id(id_ind)
        self.reload_data()
        self.view_data()

    def set_budget(self) -> None:
        """
        Метод для установки ограничений бюджета
        """
        budget_per_day = self.ui_window_set_budget.bdg_day.text()
        budget_per_week = self.ui_window_set_budget.bdg_week.text()
        budget_per_month = self.ui_window_set_budget.bdg_month.text()
        try:
            self.conn.add_a_budget_limit(budget_per_day, budget_per_week,
                                         budget_per_month)
        except ValueError:
            self.open_new_exception_window(
                "Графы с ограничением бюджета должны "
                "содержать только целые или дробные числа")
        finally:
            self.reload_data()
            self.view_data()
            self.new_window_set_budget.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpanseTracer()
    window.reload_data()
    window.show()
    sys.exit(app.exec())
