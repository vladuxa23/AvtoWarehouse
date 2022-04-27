"""
Модуль для взаимодействия с БД
"""

import pymssql
from settings import server, user, password, db

# Подключение к БД
conn = pymssql.connect(server, user, password, db)
cursor = conn.cursor(as_dict=True)


def get_tables_names() -> list:
    """
    Функция получения полного списка названий талиц

    :return: список таблиц
    """

    cursor.execute("SELECT * FROM information_schema.tables")
    table_names = []
    for row in cursor:
        table_names.append(row['TABLE_NAME'])

    return table_names


def get_all_table_data(table) -> list:
    """
    Функция получения данных из таблиц
    :param table:
    :return: список данных из таблиц
    """

    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()


def add_brand(brand_name: str) -> bool:
    """
    Функция добавления id и названия брэндов в таблицу
 TODO НЕ ПОНЯЛ ПОЧЕМУ БУЛ
    :param brand_name:
    :return: Если True то добавляет данные в таблицу, если FALSE то резит ошибку
    """

    try:
        cursor.execute("INSERT INTO brand (name) VALUES (N'%s')" % brand_name)
        conn.commit()

        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False


def add_model(model, generation) -> bool:
    """
    Функция добавления данных id и поколения в таблицу
    :param model:
    :param generation:
    :return: Если True то добавляет данные в таблицу, если FALSE то резит ошибку
    """

    try:
        cursor.execute("INSERT INTO models (name, body_code) VALUES (N'%s', N'%s')" % (model, generation))
        conn.commit()

        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False


if __name__ == '__main__':
    # ПОЛУЧЕНИЕ ДАННЫХ ИЗ ВСЕХ ТАБЛИЦ
    # for table in get_tables_names():
    #     get_all_table_data(table)



    # print(cursor.fetchall())  # показать все строки результата запроса
    conn.close()
