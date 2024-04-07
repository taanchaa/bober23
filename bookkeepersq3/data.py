"""
 Модуль содержит реализацию класса для взаимодействия с базой данных
"""
from datetime import datetime, timedelta
from PySide6 import QtWidgets, QtSql


class Controls:
    """
    Класс содержит методы реализующие взаимодействие с базой данных
    """

    def __init__(self):
        # super(Controls, self).__init__()
        super().__init__()
        self.create_connection()

    def create_connection(self):
        """
        Метод для подключения к базе данных sqlite и создания
        таблиц для хранения записей о расходах, спаска категорий
        и значений ограницения бюджета
        """
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName("Bookkeeper.db")

        if not db.open():
            QtWidgets.QMessageBox.critical(None, "Cannot open database",
                                           "Click Cancel to exit.",
                                           QtWidgets.QMessageBox.Cancel)
            return False

        request = QtSql.QSqlQuery()
        request.exec(''' CREATE TABLE IF NOT EXISTS
                Recent_expenses(OperationID INTEGER PRIMARY
                KEY AUTOINCREMENT, UpdateTime TEXT, Price REAL,
                Category TEXT,Comment TEXT)''')
        # request1 = QtSql.QSqlQuery()
        request.exec(''' CREATE TABLE IF NOT EXISTS
                Categories_storage(CategoryID INTEGER PRIMARY
                KEY AUTOINCREMENT, Category TEXT)''')

        request.exec('''CREATE TABLE IF NOT EXISTS Budget_limitation
                (LimitPerDay REAL, LimitPerWeek REAL, LimitPerMonth REAL)''')
        return True

    def create_test_connection(self):
        """
        Метод для подключения к базе данных sqlite и создания
        таблиц для хранения записей о расходах, спаска категорий
        и значений ограницения бюджета
        """
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName("Bookkeeper_test.db")

        if not db.open():
            QtWidgets.QMessageBox.critical(None, "Cannot open database",
                                           "Click Cancel to exit.",
                                           QtWidgets.QMessageBox.Cancel)
            return False
        request = QtSql.QSqlQuery()
        request.exec(''' CREATE TABLE IF NOT EXISTS
                Recent_expenses(OperationID INTEGER PRIMARY
                KEY AUTOINCREMENT, UpdateTime TEXT, Price REAL,
                Category TEXT,Comment TEXT)''')
        # request1 = QtSql.QSqlQuery()
        request.exec(''' CREATE TABLE IF NOT EXISTS
                Categories_storage(CategoryID INTEGER PRIMARY
                KEY AUTOINCREMENT, Category TEXT)''')

        request.exec('''CREATE TABLE IF NOT EXISTS Budget_limitation
                (LimitPerDay REAL, LimitPerWeek REAL, LimitPerMonth REAL)''')
        return True

    def execute_query_with_params(self, sql_query: str, query_values: list = None):
        """
        Метод для выполнения sql запросов
        """
        query = QtSql.QSqlQuery()
        query.prepare(sql_query)

        if query_values is not None:
            for query_value in query_values:
                query.addBindValue(query_value)

        query.exec()

        return query

    def add_a_category(self, new_category: str) -> None:
        """
        Метод для добавления новой категории в таблицу Categories_storage
        """
        if not new_category.isdigit():
            request = """INSERT INTO Categories_storage (Category)
                             VALUES (?);"""
            self.execute_query_with_params(request, [new_category.lower(), ])
        else:
            raise ValueError

    def add_a_position(self, price: str, category: str, comment: str = None) -> None:
        """
        Метод для добавления в таблицу Recent_expenses информации о новой операции
        """
        if price.isdigit():
            sql_query = """INSERT INTO Recent_expenses
                        (UpdateTime, Price, Category, Comment)
                        VALUES (datetime('now','+3 hour'),?,?,?);"""
            (self.execute_query_with_params
             (sql_query, [price, category, comment]))
        else:
            raise ValueError

    def delete_a_position_by_id(self, op_id: int) -> None:
        """
        Метод для удаления из базы данных операций по id операции.
        """
        request = """DELETE FROM Recent_expenses
                     WHERE OperationID = ?"""
        self.execute_query_with_params(request, [op_id, ])

    def delete_a_category_by_id(self, op_id: int) -> None:
        """
        Метод для удаления из базы данных категорий по id операции.
        """
        request = """DELETE FROM Categories_storage
                     WHERE CategoryID = ?"""
        self.execute_query_with_params(request, [op_id, ])

    def update_category(self, category_id: int, new_category: str) -> None:
        """
        Метод для изменения информации о категории по номеру id категории
        """
        if not new_category.isdigit():
            request = """UPDATE Categories_storage SET Category = ?
                                WHERE CategoryID = ?;"""
            self.execute_query_with_params(request, [new_category, category_id])
        else:
            raise ValueError

    def update_position(self, op_id: int, new_price: str,
                        new_category: str, new_comment: str) -> None:
        """
        Метод для изменения записи о расходах по номеру id операции
        """
        if new_price.isdigit():
            request = """UPDATE Recent_expenses SET Price = ?,Category = ?, Comment = ?
                         WHERE OperationID = ?;"""
            self.execute_query_with_params(request,
                                           [new_price, new_category, new_comment, op_id])
        else:
            raise ValueError

    def get_budget_per_day(self) -> str:
        """
        Метод возвращает сумму стоимостей всех операций совершенных за сегодня
        """
        date = str(datetime.now().date())
        request = """SELECT SUM(Price)
                      FROM Recent_expenses
                      WHERE strftime('%Y-%m-%d', UpdateTime) = ?;"""
        result = self.execute_query_with_params(request, [date, ])
        if result.next():
            return str(result.value(0))

        return str(0)

    def get_budget_per_week(self) -> str:
        """
        Метод возвращает сумму стоимостей всех операций совершенных за
        эту каледнарную неделю
        """
        date = (datetime.now().date() -
                timedelta(days=datetime.isoweekday(datetime.today()) - 1))
        request = """SELECT SUM(Price) FROM Recent_expenses
                      WHERE strftime('%Y-%m-%d', UpdateTime) >= ?;"""
        result = (self.execute_query_with_params(request, [str(date), ]))
        if result.next():
            return str(result.value(0))

        return str(0)

    def get_budget_per_month(self) -> str | None:
        """
        Метод возвращает сумму стоимостей всех операций совершенных за этот месяц
        """
        date = str(datetime.now().date())[:8] + '01'
        request = """SELECT SUM(Price)
                      FROM Recent_expenses
                      WHERE strftime('%Y-%m-%d', UpdateTime) >= ?;"""
        result = (self.execute_query_with_params(request, [str(date), ]))
        if result.next():
            return str(result.value(0))

        return None

    def add_a_budget_limit(self, budget_per_day: str,
                           budget_per_week: str, budget_per_month: str) -> None:
        """
        Метод для обновления данных об ограницении бюджета
        """
        if (budget_per_day.isdigit() and budget_per_week.isdigit()
                and budget_per_month.isdigit()):
            request = """UPDATE Budget_limitation SET LimitPerDay = ?,
                        LimitPerWeek = ?, LimitPerMonth = ?"""
            self.execute_query_with_params(request, [budget_per_day,
                                                     budget_per_week, budget_per_month])
        else:
            raise ValueError

        return None

    def get_a_budget_limit(self, budget_period: str) -> str | None:
        """
        Метод возвращает ограницение по бюджету за определенный период
        """
        request = f"""SELECT {budget_period} FROM Budget_limitation; """
        result = self.execute_query_with_params(request)
        if result.next():
            return str(result.value(0))
        return None

    def get_a_category_by_id(self, category_id: str) -> str:
        """
        Метод возвращает категорию по id
        """
        request = """SELECT Category FROM Categories_storage WHERE CategoryID = ?;"""
        result = self.execute_query_with_params(request, [category_id, ])
        if result.next():
            return result.value(0)
