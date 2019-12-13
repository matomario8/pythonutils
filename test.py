
from modules import *
from unittest import TestCase


class TestApp(TestCase):

    def test_date_parsing(self):

        # Test full date
        string1a = "10:30 A.M., Thursday, November 7, 2019"
        string1b = "10:30 A.M., Thursday, 11/7/2019"
        self.assertEqual(str(parse_date(string1a)), "2019:11:07")
        self.assertEqual(str(parse_date(string1b)), "2019:11:07")

        # Test day missing
        string2a = "10:30 A.M., Thursday, May, 2019"
        # string2b = "10:30 A.M., Thursday, 5/19"  # OPTIONAL
        self.assertEqual(str(parse_date(string2a)), "2019:05:01")
        # self.assertEqual(parse_date(string2b), "2019:05:01")  # OPTIONAL

        # Test month + day missing
        string3 = "10:30 A.M., Thursday, 2019"
        self.assertEqual(str(parse_date(string3)), "2019:01:01")

        # Test that no date returns blank
        string4 = "10:30 A.M., Thursday"
        self.assertEqual(str(parse_date(string4)), "")





    def test_time_parsing(self):

        # Test valid times
        string1 = "10:30 A.M., Thursday, November 7, 2019"
        string2 = "10:30 PM, Thursday, November 7, 2019"
        self.assertEqual(parse_time(string1), "10:30:00")
        self.assertEqual(parse_time(string2), "22:30:00")

        # Test empty time
        string3 = ", Thursday, November 7, 2019"
        self.assertEqual(parse_time(string3), "00:00:00")

        # TODO: Extending parse_time() to include 24 hour clock format


