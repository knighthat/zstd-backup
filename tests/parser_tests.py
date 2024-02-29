import unittest

from src import parser


class DateParsingTests(unittest.TestCase):
    valid_dates = [
        "2024-Feb-24 00-01-000001",
        "2024-Feb-25 00-02-000002",
        "2024-Feb-26 00-03-000003",
        "2024-Feb-27 00-04-000004",
        "2024-Feb-28 00-05-000005",
        "2024-Feb-29 00-06-000006",
        "2024-Mar-01 00-07-000007",
        "2024-Mar-02 00-08-000008",
        "2024-Mar-03 00-09-000009",
        "2024-Mar-04 00-10-000010",
    ]
    invalid_dates = [
        "24-Feb-2024 08-15-000000",
        "File1",
        "06-Apr-2024 19-25-000000",
        "Unk-2-2024 10-30-000000",
        "19-Jun-2024 05-35-000000",
        "11-Jul-2024 20-40-000000",
        "2024-Mar-03 26-09-000009",
        "25-Sep-2024 11-50-000000",
        "17-Oct-2024 06-55-000000",
        "Nov-08-2024 22-00-000000",
    ]

    def test_valid_parse_date(self) -> None:
        for date in self.valid_dates:
            try:
                parser.parse_date(date)
            except:
                self.fail(f'{date} is invalid!')

    def test_invalid_parse_date(self) -> None:
        for date in self.invalid_dates:
            try:
                parser.parse_date(date)
                self.fail(f'{date} is valid!')
            except:
                continue


if __name__ == '__main__':
    unittest.main()
