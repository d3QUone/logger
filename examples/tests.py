__author__ = 'vladimir'

import time
import subprocess
import unittest

import requests


class AppMainTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Run the server-app"""
        cls.Unit = subprocess.Popen(["venv/bin/gunicorn", "app:api"])
        print "server PID is {0}".format(cls.Unit.pid)
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        """Kill test-unit"""
        print "killing..."
        cls.Unit.kill()

    def test_CRUD(self):
        url = "http://127.0.0.1:8000/user"
        profiles = (
            {
                "slug": "user1",
                "name": "John",
                "email": "john-user@yandex.ru",
                "group": 4
            },
            {
                "slug": "user2",
                "name": "Max",
                "email": "max-user@mail.ru",
                "group": 4
            },
            {
                "slug": "user3",
                "name": "Koff",
                "email": "noname@mail.ru",
                "group": 3
            },
        )
        # create - OK
        for user in profiles:
            res = requests.post(url, user).json()
            self.assertTrue(res["success"])

        # repeat, assert fail
        for user in profiles:
            res = requests.post(url, user).json()
            self.assertFalse(res["success"])

        # get all users
        res = requests.get(url).json()
        self.assertEqual(len(res), len(profiles))


if __name__ == "__main__":
    unittest.main()
