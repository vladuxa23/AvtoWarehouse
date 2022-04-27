import json
import os

import models as mdb


def get_cache():
    """
    Получение всех данных из cache (json)

    :return: словарь своварей данных из БД
    """

    all_cache_data = {}
    for file_ in os.listdir("cache"):

        with open(os.path.join('cache', file_), "r") as f:
            data = json.load(f)

        all_cache_data.update(data)

    return all_cache_data


def get_brands(cache: dict) -> list:
    """
    Получение всех брэндов из загруженного кэша

    :param cache:
    :return:список брэндов
    """

    brands = set()
    for key in cache:
        if cache[key].get('Брэнд'):
            brands.add(cache[key].get('Брэнд'))

    return list(brands)


def get_models(cache: dict) -> list:
    """
    Функция по ключу вытаскивает все модели и поколения (за исключением дублей)
    :param cache:
    :return:
    """

    brands = set()
    for key in cache:
        if cache[key].get('Поколение:'):
            brands.add((cache[key].get('Модель'), cache[key].get('Поколение:')))

    return list(brands)

def get_drive_type(cache: dict) -> list:
    """
    Функция по ключу вытаскивает тип привода а/м (за исключением  дублей)
    :param cache:
    :return: типы приводов для всех автомобилей в словаре
    """
    drive = set()
    for key in cache:
        if cache[key].get('Привод:'):
            drive.add((cache[key].get('Привод:')))

    return list(drive)


if __name__ == '__main__':
    ALL_CACHE = get_cache()
    get_brands(ALL_CACHE)

    # ЗАГРУЗКА ДАННЫХ В ТАБЛИЦУ brands
    # for brand in get_brands(ALL_CACHE):
    #     mdb.add_brand(brand)

    # ЗАГРУЗКА ДАННЫХ В models
    # for model in get_models(ALL_CACHE):
    #     mdb.add_model(*model)

    #ЗАГРУЗКА ДАННЫХ В complectation
    # for drive in get_drive_type(ALL_CACHE):
    #     mdb.add_drive_type(drive)

    # get_drive_type(ALL_CACHE)





    mdb.conn.close()
