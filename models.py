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
    Функция получения полного списка названий таблиц

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


def add_model(model, generation, brand_id) -> bool:
    """
    Функция добавления данных id и поколения в таблицу
    :param model:
    :param generation:
    :return: Если True то добавляет данные в таблицу, если FALSE то резит ошибку
    """

    try:
        cursor.execute("INSERT INTO models (name, body_code, brand_id) VALUES (N'%s', N'%s', %d)" % (model, generation, brand_id))
        conn.commit()

        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False


def add_drive_type(drive) -> bool:
    """
    Функция добавления данных id и типа привода в таблицу
    :return:Если True то добавляет данные в таблицу, если FALSE то резит ошибку
    """
    try:
        cursor.execute("INSERT INTO drive_type(type) VALUES (N'%s')" % drive)
        conn.commit()
        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False


def add_engine_type(engine_type) -> bool:
    """
    Функция добавления данных id и типа двигателя в таблицу
    :return:Если True то добавляет данные в таблицу, если FALSE то резит ошибку
    """
    try:
        cursor.execute("INSERT INTO engine_type(type) VALUES (N'%s')" % (engine_type))
        conn.commit()
        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False


def add_transmission_type(transmission_type) -> bool:
    """
    Функция добавления данных id и типа коробки передач в базу
    :param transmission_type:
    :return: Если True то добавляет данные в таблицу, если FALSE то резит ошибку
    """
    try:
        cursor.execute("INSERT INTO transmission_type(type) VALUES (N'%s')" % (transmission_type))
        conn.commit()
        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False

def add_model_list(model_id):
    try:
        brand_id = get_brand_id_by_model_id(model_id)
        cursor.execute("INSERT INTO model_list(model_id, brand_id) VALUES (%d, %d)" % (model_id, brand_id))
        conn.commit()
        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False

def get_brand_id_by_model_id(model_id):
    cursor.execute("SELECT brand_id FROM models WHERE id = %d" % model_id)
    data = cursor.fetchall()
    return data[0]["brand_id"]

def get_brand_id_by_brand(brand: str) -> int:
    cursor.execute("SELECT id from brand  where name = N'%s'" % brand)
    data = cursor.fetchall()
    return data[0]['id']


def get_all_brands():
    cursor.execute("SELECT name FROM brand")
    data = cursor.fetchall()
    return [elem['name'] for elem in data]


def get_model_id_by_model(model: str) -> int:
    cursor.execute("SELECT id from models  where name = N'%s'" % model)
    data = cursor.fetchall()
    return data[0]['id']


def get_all_models() -> list:
    cursor.execute("SELECT name FROM models")
    data = cursor.fetchall()
    return [elem['name'] for elem in data]

def get_model_list_id() -> list:
    cursor.execute("SELECT id FROM model_list")
    data = cursor.fetchall()
    return data[0]['id']

def get_model_list_id_by_brand_and_model(brand, model):
    # cursor.execute("SELECT id FROM brand WHERE id = %d" % brand)
    cursor.execute("SELECT name FROM brand and SELECT model FROM models WHERE id = %d" % model)
    data = cursor.fetchall()
    return data[0]['id']

def get_engine_type_id_by_name() -> list:
    ...


    # cursor.execute("SELECT brand_id FROM models WHERE id = %d" % model_id)
    # data = cursor.fetchall()
    # return data[0]["brand_id"]

def get_drive_type_id_by_name() -> list:
    ...

def get_transmission_type_id_by_name() -> list:
    ...

def add_complectation(complectation):
    ...



if __name__ == '__main__':
    # ПОЛУЧЕНИЕ ДАННЫХ ИЗ ВСЕХ ТАБЛИЦ
    # for table in get_tables_names():
    #     get_all_table_data(table)
    # get_brand_id_by_brand('Audi')
    # print(get_model_id_by_model('Matiz'))

    # print(get_all_brands())
    # get_model_list_id()
    get_model_list_id_by_brand_and_model('Daewoo', 'Matiz')

    # print(cursor.fetchall())  # показать все строки результата запроса
    conn.close()
