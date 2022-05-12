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

    clear_all_cache_data = {key: value for key, value in all_cache_data.items() if len(value) > 2}

    return clear_all_cache_data


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
            brands.add((cache[key].get('Модель'), cache[key].get('Поколение:'),
                        mdb.get_brand_id_by_brand(cache[key].get('Брэнд'))))

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


def get_engine_type(cache: dict) -> list:
    """
    Функция по ключу вытаскивает тип двигателя а/м (за исключением  дублей)
    :param cache:
    :return: типы двигателей для всех автомобилей в словаре
    """
    engine_type = set()
    for key in cache:
        if cache[key].get('Тип двигателя:'):
            engine_type.add(cache[key].get('Тип двигателя:'))

    return list(engine_type)


def get_transmission_type(cache: dict) -> list:
    """
    Функция по ключу вытаскивает тип коробки передач а/м (за исключением дублей)
    :param cache:
    :return: типы коробок передач для всех автомобилей в словаре
    """
    transmission_type = set()
    for key in cache:
        if cache[key].get("Коробка передач:"):
            transmission_type.add(cache[key].get("Коробка передач:"))
    return list(transmission_type)


def get_complectation(cache: dict) -> list:
    complectation = set()
    for key in cache:
        if cache[key].get("Брэнд"):
            complectation.add(
                (cache[key].get("Брэнд"), cache[key].get("Модель"), cache[key].get("Комплектация:", "Отсутствует"),
                 cache[key].get("Тип двигателя:"), cache[key].get("Привод:"), cache[key].get("Коробка передач:")))
    return list(complectation)


def get_avto(cache: dict) -> list:
    avto = set()
    for key in cache:
        if cache[key].get("Брэнд"):
            avto.add((cache[key].get("Брэнд"), cache[key].get("Модель"), cache[key].get("Пробег:"),
                      cache[key].get("Владельцев по ПТС:"), cache[key].get("Модификация:"),
                      cache[key].get("Цвет:"), cache[key].get("Тип двигателя:"), cache[key].get("Коробка передач:"),))
    return list(avto)


if __name__ == '__main__':
    ALL_CACHE = get_cache()
    # get_brands(ALL_CACHE)

    # ЗАГРУЗКА ДАННЫХ В ТАБЛИЦУ brands
    # for brand in get_brands(ALL_CACHE):
    #     mdb.add_brand(brand)

    # ЗАГРУЗКА ДАННЫХ В models
    # for model in get_models(ALL_CACHE):
    #     mdb.add_model(*model)

    # ЗАГРУЗКА ДАННЫХ В drive_type
    # for drive in get_drive_type(ALL_CACHE):
    #     mdb.add_drive_type(drive)

    # ЗАГРУЗКА ДАННЫХ в engine_type
    # for engine_type in get_engine_type(ALL_CACHE):
    #     mdb.add_engine_type(engine_type)

    # ЗАГРУЗКА ДАННЫХ в transmission_type
    # for transmission_type in get_transmission_type(ALL_CACHE):
    #     mdb.add_transmission_type(transmission_type)

    # ЗАГРУЗКА ДАННЫХ в model_list
    # for model in mdb.get_all_models():
    #     mdb.add_model_list(mdb.get_model_id_by_model(model))

    # ЗАГРУЗКА ДАННЫХ в complectation
    # for complectation in get_complectation(ALL_CACHE):
    #     mdb.add_complectation(complectation)

    # ЗАГРУЗКА ДАННЫХ в avto
    # for avto in get_avto(ALL_CACHE):
    #     mdb.add_avto(avto)

    # get_drive_type(ALL_CACHE)

    # get_avto(ALL_CACHE)

    # get_complectation(ALL_CACHE)

    mdb.conn.close()
