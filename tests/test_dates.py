#-*- coding: utf-8 -*-
import unittest
from datetime import date
from period import parse

class TestDates(unittest.TestCase):

    def test_century(self):
        self.assertEqual(parse('19').starting, date(1901, 1, 1))

    def test_year(self):
        self.assertEqual(parse('1985').starting, date(1985, 1, 1))

    def test_month(self):
        self.assertEqual(parse('1985-04').starting, date(1985, 4, 1))

    def test_base_complete(self):
        self.assertEqual(parse('1985-04-12').starting, date(1985, 4, 12))
        self.assertEqual(parse('19850412').starting, date(1985, 4, 12))
        self.assertEqual(parse('1985102').starting, date(1985, 4, 12))
        self.assertEqual(parse('1985-102').starting, date(1985, 4, 12))
    
    def test_week_complete_and_ext(self):
        self.assertEqual(parse('1985W155').starting, date(1985, 4, 12))
        self.assertEqual(parse('1985-W15-5').starting, date(1985, 4, 12))
        self.assertEqual(parse('1985W15').starting, date(1985, 4, 8))
        self.assertEqual(parse('1985-W15').starting, date(1985, 4, 8))
        self.assertEqual(parse('1989-W15').starting, date(1989, 4, 10))
        self.assertEqual(parse('1989-W15-5').starting, date(1989, 4, 14))

    def test_expanded_century(self):
        self.assertEqual(parse('+0019').starting, date(1901, 1, 1))

    def test_expanded_year(self):
        self.assertEqual(parse('+001985').starting, date(1985, 1, 1))

    def test_expanded_month(self):
        self.assertEqual(parse('+001985-04').starting, date(1985, 4, 1))

    def test_expanded_complete(self):
        self.assertEqual(parse('+001985-04-12').starting, date(1985, 4, 12))
        self.assertEqual(parse('+0019850412').starting, date(1985, 4, 12))
        self.assertEqual(parse('+001985102').starting, date(1985, 4, 12))
        self.assertEqual(parse('+001985-102').starting, date(1985, 4, 12))

    def test_expanded_week_complete_and_ext(self):
        self.assertEqual(parse('+001985W155').starting, date(1985, 4, 12))
        self.assertEqual(parse('+001985-W15-5').starting, date(1985, 4, 12))
        self.assertEqual(parse('+001985W15').starting, date(1985, 4, 8))
        self.assertEqual(parse('+001985-W15').starting, date(1985, 4, 8))
