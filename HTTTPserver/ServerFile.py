import os.path
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

from sys import path
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


class BankCheckerServer(BaseHTTPRequestHandler):
    """
    Реализация HTTP-сервера для обработки запросов.
    """

    def do_GET(self):
        """
        Реализация ответа на Get запрос.\n
        """
        input_number = query_decode(self.requestline)
        check_input_number = query_validator(input_number)
        if check_input_number:
            answer = make_json(dataBase.search_bank_by_value(int(str(input_number)[:6])))
            self.send_response(200, "Answer is ready")
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(answer.encode("utf-8"))
        else:
            self.send_response(500, "Incorrect Number")


# Если не было введено других аргументов при запуске программы, будет использована внутренняя БД.
file_from_arg = sys.argv[0]
if os.path.exists(file_from_arg):
    path = file_from_arg
else:
    print("Указанного файла по этому адресу не существует. Выбрана внутренняя БД.")
    path = os.path.abspath('..\\DB_holder\\binlist-data.csv')
print(sys.argv)
dataBase = DataBaseHolder(path)
try:
    dataBase.parse_file()
except ParserError:
    print("Произошла ошибка в ходе чтения файла.\nБудет использована внутренняя БД.")
    path = os.path.abspath('..\\DB_holder\\binlist-data.csv')
    dataBase = DataBaseHolder(path)
    dataBase.parse_file()
serv = HTTPServer(("localhost", 80), BankCheckerServer)
serv.serve_forever()
