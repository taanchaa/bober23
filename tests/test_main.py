import pytest
from bookkeepersq3.data import Controls
import sqlite3

control = Controls()


@pytest.fixture
def db_connect():
    control.create_test_connection()
    conn = sqlite3.connect('bookkeeper_test.db')
    # cursor = conn.cursor()
    # cursor.execute('''CREATE TABLE IF NOT EXISTS Recent_expenses(
    #                 OperationID INTEGER PRIMARY KEY AUTOINCREMENT,
    #                 UpdateTime TEXT, Price REAL,
    #                 Category TEXT,Comment TEXT)''')
    # conn.commit()
    yield conn
    conn.close()


def test_add_a_position(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Recent_expenses""")
    db_connect.commit()
    control.add_a_position('100', 'Хозтовары', 'Пакет')
    cursor.execute("SELECT * FROM Recent_expenses WHERE Category='Хозтовары'")
    result = cursor.fetchone()
    assert result is not None


def test_delete_a_position_by_id(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Recent_expenses""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime(),'100','Хозтовары','Пакет');""")
    db_connect.commit()
    cursor.execute("""SELECT MAX(OperationID) FROM Recent_expenses""")
    max_id = cursor.fetchone()
    control.delete_a_position_by_id(max_id[0])
    cursor.execute("""SELECT * FROM Recent_expenses WHERE OperationID = 
                   (SELECT MAX(OperationID) FROM Recent_expenses)""")
    result = cursor.fetchone()
    assert result is None


def test_update_category(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Categories_storage""")
    db_connect.commit()

    cursor.execute("""INSERT INTO Categories_storage (Category)
                      VALUES ('Хозтовары');""")
    db_connect.commit()
    cursor.execute("""SELECT MAX(CategoryID) FROM Categories_storage""")
    max_id = cursor.fetchone()
    control.update_category(max_id[0], 'Продукты')
    cursor.execute("""SELECT Category FROM Categories_storage WHERE CategoryID = 
                   (SELECT MAX(CategoryID) FROM Categories_storage);""")
    result = cursor.fetchone()
    assert result[0] == 'Продукты'


def test_update_position(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Recent_expenses""")
    db_connect.commit()

    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime(),100,'Хозтовары','Пакет');""")
    db_connect.commit()
    cursor.execute("""SELECT MAX(OperationID) FROM Recent_expenses""")
    max_id = cursor.fetchone()
    control.update_position(max_id[0], '200', 'Транспорт', 'Билет')
    cursor.execute("""SELECT Price, Category, Comment FROM Recent_expenses WHERE OperationID = 
                   (SELECT MAX(OperationID) FROM Recent_expenses);""")
    result = cursor.fetchmany()
    assert result[0][0] == 200.0 and result[0][1] == 'Транспорт' and result[0][2] == 'Билет'


def test_budget_per_day(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Recent_expenses""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime(),100,'Хозтовары','Пакет');""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime(),200,'Хозтовары','Пакет');""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime('2024-03-27 17:44:45'),300,'Хозтовары','Пакет');""")
    db_connect.commit()
    assert control.get_budget_per_day() == str(300.0)


def test_budget_per_week(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Recent_expenses""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime(),100,'Хозтовары','Пакет');""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime(),200,'Хозтовары','Пакет');""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime('2020-01-01 12:00:00'),1000,'Хозтовары','Пакет');""")
    db_connect.commit()
    assert control.get_budget_per_week() == str(300.0)


def test_budget_per_month(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Recent_expenses""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime(),100,'Хозтовары','Пакет');""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime(),200,'Хозтовары','Пакет');""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Recent_expenses (UpdateTime, Price, Category, Comment)
                      VALUES (datetime('2020-01-01 12:00:00'),300,'Хозтовары','Пакет');""")
    db_connect.commit()
    assert control.get_budget_per_month() == str(300.0)


def test_add_a_budget_limit(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Budget_limitation""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Budget_limitation (LimitPerDay, LimitPerWeek, LimitPerMonth)
                      VALUES (100,200,300);""")
    db_connect.commit()
    control.add_a_budget_limit(str(200), str(300), str(400))
    cursor.execute("""SELECT LimitPerDay, LimitPerWeek, LimitPerMonth FROM Budget_limitation;""")
    result = cursor.fetchmany()
    assert result[0][0] == 200.0 and result[0][1] == 300.0 and result[0][2] == 400.0
    db_connect.commit()


def test_get_a_budget_limit(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Budget_limitation""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Budget_limitation (LimitPerDay, LimitPerWeek, LimitPerMonth)
                          VALUES (100,200,300);""")
    db_connect.commit()
    assert control.get_a_budget_limit('LimitPerWeek') == str(200.0)

def test_get_a_category_by_id(db_connect):
    cursor = db_connect.cursor()
    cursor.execute("""DELETE FROM Categories_storage""")
    db_connect.commit()
    cursor.execute("""INSERT INTO Categories_storage (Category)
                              VALUES ('Хозтовары');""")
    db_connect.commit()
    cursor.execute("""SELECT MAX(CategoryID) FROM Categories_storage""")
    max_id = cursor.fetchone()
    assert control.get_a_category_by_id(max_id[0]) == 'Хозтовары'
