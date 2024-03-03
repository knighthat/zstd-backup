import unittest

from src.converter import size_converter, time_converter


class SizeConverterTest(unittest.TestCase):
    values: dict = {
        123964695035118467: '110.1 PiB',
        718738095144875397043302: '608.79 ZiB',
        106900107238: '99.56 GiB',
        76677045350896076170964: '64.95 ZiB',
        4950007542014806: '4.4 PiB',
        53216041131825978: '47.27 PiB',
        620972000: '592.21 MiB',
        935196920133407533468642: '792.14 ZiB',
        497970824908441: '452.9 TiB',
        10040025365881342327306: '8.5 ZiB',
        4697760172434888: '4.17 PiB',
        1184: '1.16 KiB',
        44: '44.0 B',
        45868521606000: '41.72 TiB',
        62274434492409145038264: '52.75 ZiB',
        4293307635994226810999: '3.64 ZiB',
        83361787014847490: '74.04 PiB',
        156934193656961743949518: '132.93 ZiB',
        5518656958621443: '4.9 PiB',
        11142063381898668: '9.9 PiB'
    }

    def test_size_converter(self):
        for size_b, string in self.values.items():
            self.assertEqual(size_converter(size_b), string)


class TimeConverterTest(unittest.TestCase):
    values: dict = {
        956197.496: '265 hours 36 minutes 37 seconds',
        474104.98: '131 hours 41 minutes 45 seconds',
        794202.525: '220 hours 36 minutes 43 seconds',
        188280.449: '52 hours 18 minutes',
        922740.641: '256 hours 19 minutes 1 second',
        49513.291: '13 hours 45 minutes 13 seconds',
        244223.706: '67 hours 50 minutes 24 seconds',
        573178.119: '159 hours 12 minutes 58 seconds',
        573831.513: '159 hours 23 minutes 52 seconds',
        265498.12: '73 hours 44 minutes 58 seconds',
        628914.457: '174 hours 41 minutes 54 seconds',
        991340.38: '275 hours 22 minutes 20 seconds',
        27666.192: '7 hours 41 minutes 6 seconds',
        190202.947: '52 hours 50 minutes 3 seconds',
        881200.232: '244 hours 46 minutes 40 seconds',
        427917.347: '118 hours 51 minutes 57 seconds',
        851527.946: '236 hours 32 minutes 8 seconds',
        237251.585: '65 hours 54 minutes 12 seconds',
        993914.205: '276 hours 5 minutes 14 seconds',
        548971.598: '152 hours 29 minutes 32 seconds'
    }

    def test_time_converter(self):
        for second, string in self.values.items():
            self.assertEqual(time_converter(second), string)


if __name__ == '__main__':
    unittest.main()
