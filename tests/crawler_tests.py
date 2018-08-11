import unittest
from crawler import *
import os

class Scraper_tests(unittest.TestCase):
    test_data = "$Thwumpwards IV#Hindi#minimalism#00000000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\
000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000|5^396,540!8^420,5\
40,3!8^372,540,3!11^396,444,396,156!8^396,516,3!0^396,60#"

    def test_scrape(self):
        data, labels = scrape(238130)
        self.assertEqual(data, self.test_data)
        self.assertEqual(labels, ["author:hindi", "minimalism", "symmetrical", "thwumpwards", "unrated", "id:238130"])

    def test_persist(self):
        with open("numa_archive.csv", 'a') as csv_file:
            persist("leveldata", ["label1", "label2"], csv_file)
        with open("numa_archive.csv") as csv_file:
            firstline = csv_file.readlines()[0]
            self.assertEqual(firstline.rstrip(), "leveldata;label1,label2")

    def test_data_in_expected_format(self):
        self.assertTrue(data_in_expected_format(self.test_data))
        self.assertFalse(data_in_expected_format(self.test_data[20:]))

    def tearDown(self):
        if os.path.isfile("numa_archive.csv"):
            os.remove("numa_archive.csv")