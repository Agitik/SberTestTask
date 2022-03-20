import os.path
import unittest
from DB_holder.DB_holder import *
from QueryPreparation.WorkingWithQuery import *

testBase = DataBaseHolder(os.path.abspath("../DB_holder/binlist-data.csv"))


class Test_different_numbers(unittest.TestCase):
    def setUp(self) -> None:
        global testBase
        testBase.parse_file()

    def test_ideal(self):
        testResult = testBase.search_bank_by_value(427655)
        waitingResult = "{'Country': 'RUSSIA', 'Bank': 'SAVINGS BANK OF THE RUSSIA (SBERBANK)', 'Latitude': 61.524, 'Longitude': 105.319, 'Phone': '-', 'URL': '-'}"
        assert (testResult, waitingResult)

    def test_incorrect_test(self):
        testResult = testBase.search_bank_by_value(000000)
        waitingResult = "No result!"
        assert (testResult, waitingResult)

    def test_query_validator_good(self):
        assert (query_validator("4276550038471176"), True)

    def test_query_validator_big_number(self):
        assert (query_validator("427655003847117623455"), False)

    def test_query_validator_little_number(self):
        assert (query_validator("2332"), False)




