import unittest

import requests


class MyTestCase(unittest.TestCase):
    def test_normal_work(self):
        response = requests.get('http://localhost/cards/4276550038471176')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
