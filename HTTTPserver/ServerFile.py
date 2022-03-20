import os.path
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from pandas.errors import ParserError
from QueryPreparation.WorkingWithQuery import *
from GlobalLogger.Logger import *
from DB_holder.DB_holder import *


def query_decode(httpreq):
    """
    Получает номер карты.\n
    :param httpreq: http запрос от клиента в формате "GET /cards/*** HTTP/1.1"
    :return: список формата "[GET, cards, ****,...]
    """
    return httpreq.split(" ")[1].split("/")[2]


def path_pointer() -> str:
    """
    Проверяет, был ли передан путь к файлу с базой данных через аргументы ком. строки.\n
    Если файл не был передан или получен некорректный путь к файлу, сервер будет работать со старой БД.\n
    :return: путь к файлу
    """
    path = os.path.abspath('DB_holder\\binlist-data.csv')
    try:
        file_from_arg = sys.argv[1]
        if os.path.exists(file_from_arg):
            path = file_from_arg
        else:
            print("Указанного файла по этому адресу не существует. Выбрана внутренняя БД.")
    except IndexError:
        print("Не был указан файл в аргументе командной строки. Будет использована старая БД.")
    return path


database = 0


class BankCheckerServer(BaseHTTPRequestHandler):
    """
    Реализация HTTP-сервера для обработки запросов.
    """

    def do_GET(self):
        """
        Реализация ответа на Get запрос.\n
        """
        global database
        input_number = query_decode(self.requestline)
        check_input_number = query_validator(input_number)
        if check_input_number:
            answer = make_json(database.search_bank_by_value(int(str(input_number)[:6])))
            self.send_response(200, "Answer is ready")
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(answer.encode("utf-8"))
        else:
            self.send_response(500, "Incorrect Number")


def prestart_action():
    """
    Парсит файл базы данных и в случае неудачного парсинга выбирает старую базу данных.
    """
    global database
    database = DataBaseHolder(path_pointer())
    try:
        database.parse_file()
    except ParserError:
        print("Произошла ошибка в ходе чтения файла.\nБудет использована внутренняя БД.")
        path = os.path.abspath('DB_holder\\binlist-data.csv')
        database = DataBaseHolder(path)
        database.parse_file()


def start_server(ip: str = 'localhost', port: int = 80):
    """
    Запуск сервера
    :param ip: адрес сервера
    :param port: порт
    """
    prestart_action()
    serv = HTTPServer((ip, port), BankCheckerServer)
    print(f"Запущен сервер. Адрес: {ip}. Порт: {port}.")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Сервер заершает свою работу по запросу!")
        serv.shutdown()
