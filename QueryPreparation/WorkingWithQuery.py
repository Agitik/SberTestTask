import json


def make_json(answer) -> json:
    """
    Данный метод упаковывает словарь, полученный в качестве ответа DB_holder в json объект.\n
    :param answer: ответ на запрос к базе данных.
    :return: упакованный в JSON ответ на запрос к базе данных.
    """
    return json.dumps(answer)


def query_validator(query):
    """
    Данный метод проверяет полученный номер карты на возможность использования в дальнейшем.\n
    :param query: номер карты от сервера.
    :return: true - можно использовать для запроса к БД, false - нельзя использовать для запроса к БД.
    """
    ret = 0
    query = ''.join(str(query).split())
    try:
        query = int(query)
        if 16 <= len(str(query)) <= 20:
            ret = True
        else:
            ret = False
    except ValueError:
        ret = False
    return ret

