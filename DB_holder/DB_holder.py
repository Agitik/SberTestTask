from GlobalLogger.Logger import logger
import pandas as pd


class DataBaseHolder:
    """
    Данный класс предназначен для работы с полученной базой данных.
    """

    data_from_file = 0

    def __init__(self, dbfilepath):
        """
        Создает экземпляр класса через путь к файлу базы данных.\n
        :param dbfilepath: ссылка на документ с базой данных.
        """
        self.dbFilePath = dbfilepath
        logger.info(f"\nСоздан объект класса DataBaseHolder.\nТип БД: csv.\n")

    def parse_file(self):
        """
        Данный метод читает csv файл с базой данных.
        И присваивает переменной класса DataFrame, основанный на парсинге файла БД.
        """
        data = pd.read_csv(self.dbFilePath, sep=',')
        logger.info(f"\nФайл, расположеннный по пути: '{self.dbFilePath}' прочитан.\nПолучено: {len(data)} строк.\n")
        self.data_from_file = data

    def search_bank_by_value(self, card_prefix) -> dict:
        """
        Данный метод предназначен для поиска значения в таблице.\n
        :param card_prefix: 6 цифр BIN-номера карты.
        :return: cловарь с информацией о банке.
        """
        search_result = self.data_from_file.loc[self.data_from_file['bin'] == card_prefix]
        logger.info(
            f"\nБыл произведен поиск банка по значению BIN номера карты.\nВходной bin: {card_prefix}.")
        try:
            bank_info = {
                'Country': search_result['country'].values[0],
                'Bank': search_result['issuer'].values[0],
                'Latitude': search_result['latitude'].values[0],
                'Longitude': search_result['longitude'].values[0],
                'Phone': search_result['bank_phone'].values[0],
                'URL': search_result['bank_url'].values[0]
            }

            for key, value in bank_info.items():
                if str(value) == 'nan':
                    bank_info[key] = '-'

        except (IndexError, KeyError):
            bank_info = "No results!"
        return bank_info
