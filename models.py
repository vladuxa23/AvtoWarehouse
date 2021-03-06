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
        cursor.execute(
            "INSERT INTO models (name, body_code, brand_id) VALUES (N'%s', N'%s', %d)" % (model, generation, brand_id))
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


def add_complectation(complectation):
    brand_model = get_model_list_id_by_brand_and_model(complectation[0], complectation[1])
    eng_type = get_engine_type_id_by_name(complectation[3])
    drive_type = get_drive_type_id_by_name(complectation[4])
    transmission_type = get_transmission_type_id_by_name(complectation[5])
    try:
        cursor.execute("INSERT INTO complectation(model_list_id, name, engine_type_id, drive_type_id, transmission_type_id)\
                       VALUES (%d, N'%s', %d, %d, %d)" % (
        brand_model, complectation[2], eng_type, drive_type, transmission_type))
        conn.commit()
        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False


def add_avto(avto):

    model_list_id = get_model_list_id_by_brand_and_model(avto[0], avto[1])
    mileage = avto[2]
    owners_count = avto[3]
    engin_capacity = avto[4]
    body_color = avto[5]
    complectation_id = get_complectation_id(model_list_id, avto[8], avto[6], avto[9], avto[7])

    try:
        cursor.execute("INSERT INTO avto(model_list_id, mileage, owners_count, engine_capacity, body_color, complectation_id)\
                       VALUES (%d, %d,  %d, N'%s',N'%s', %d)" % (model_list_id, mileage, owners_count, engin_capacity, \
                                                                 body_color, complectation_id))
        conn.commit()
        return True
    except pymssql._pymssql.IntegrityError as err:
        print(err)
        return False

def get_complectation_id(mod_lst_id, complectation_name, engine, drive_t, transmission):

    engine_type_id = get_engine_type_id_by_name(engine)
    drive_type_id = get_drive_type_id_by_name(drive_t)
    transmission_type_id = get_transmission_type_id_by_name(transmission)
    cursor.execute ("SELECT id FROM complectation WHERE model_list_id =%d and name = N'%s' and engine_type_id =%d and \
                    drive_type_id =%d and transmission_type_id =%d" % (mod_lst_id, complectation_name, engine_type_id, drive_type_id,\
                    transmission_type_id))
    data = cursor.fetchall()
    return data[0]['id']



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


def get_model_list_id_by_brand_and_model(brand, model) -> int:
    cursor.execute("SELECT id FROM brand WHERE name = N'%s'" % brand)
    brand_id = cursor.fetchall()[0]["id"]

    cursor.execute("SELECT id FROM models WHERE name = N'%s'" % model)
    model_id = cursor.fetchall()[0]["id"]

    cursor.execute("SELECT id FROM model_list WHERE brand_id = %d AND model_id = %d" % (brand_id, model_id))
    model_list_id = cursor.fetchall()[0]['id']

    return model_list_id


def get_engine_type_id_by_name(type: str) -> int:
    cursor.execute("SELECT id FROM engine_type WHERE type = N'%s'" % type)
    data = cursor.fetchall()
    return data[0]["id"]


def get_drive_type_id_by_name(type: str) -> int:
    cursor.execute("SELECT id FROM drive_type WHERE type = N'%s'" % type)
    data = cursor.fetchall()
    return data[0]["id"]


def get_transmission_type_id_by_name(type: str) -> int:
    cursor.execute("SELECT id FROM transmission_type WHERE type = N'%s'" % type)
    data = cursor.fetchall()
    return data[0]["id"]


if __name__ == '__main__':
    # ПОЛУЧЕНИЕ ДАННЫХ ИЗ ВСЕХ ТАБЛИЦ
    # for table in get_tables_names():
    #     get_all_table_data(table)
    # get_brand_id_by_brand('Audi')
    # print(get_model_id_by_model('Matiz'))

    # print(get_all_brands())
    # get_model_list_id()
    # get_model_list_id_by_brand_and_model('Daewoo', 'Matiz')
    # get_engine_type_id_by_name('Бензин')
    # get_drive_type_id_by_name('Полный')
    # get_transmission_type_id_by_name('Автомат')
    # add_avto()
    get_complectation_id('Volkswagen', 'Polo', 'Отсутствует', 'Бензин', 'Передний', 'Механика')
    # add_avto()

    # print(cursor.fetchall())  # показать все строки результата запроса
    conn.close()
