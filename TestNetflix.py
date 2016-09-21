#!/usr/bin/env python3

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------
import pickle
import sys

from io       import StringIO
from unittest import main, TestCase

from Netflix import netflix_read, netflix_eval, netflix_print, netflix_solve, get_rmse

class TestNetflix (TestCase) :
    # ----
    # read
    # ----

    def test_read1 (self) :
        s    = "342:\n"
        i = netflix_read(s)
        self.assertEqual(i,  "342:")

    def test_read2 (self) :
        s    = "564576\n"
        i = netflix_read(s)
        self.assertEqual(i,  "564576")

    def test_read3 (self) :
        s    = "2\n"
        i = netflix_read(s)
        self.assertEqual(i,  "2")

    def test_read4 (self) :
        s    = "4563456\n"
        i = netflix_read(s)
        self.assertEqual(i,  "4563456") 

    def test_read5 (self) :
        s    = "4563456:\n"
        i = netflix_read(s)
        self.assertEqual(i,  "4563456:") 

    def test_read6 (self) :
        s    = "1:\n"
        i = netflix_read(s)
        self.assertEqual(i,  "1:")

    # -----
    # print
    # -----

    def test_print1 (self) :
        w = StringIO()
        netflix_print(w, "10:", -1)
        self.assertEqual(w.getvalue(), "10:\n")

    def test_print2 (self) :
        w = StringIO()
        netflix_print(w, "10045", 5.0)
        self.assertEqual(w.getvalue(), "5.0\n")

    def test_print3 (self) :
        w = StringIO()
        netflix_print(w, "1", 1.0)
        self.assertEqual(w.getvalue(), "1.0\n")

    def test_print4 (self) :
        w = StringIO()
        netflix_print(w, "4567", 4.3)
        self.assertEqual(w.getvalue(), "4.3\n")

    def test_print5 (self) :
        w = StringIO()
        netflix_print(w, "1234:", -1)
        self.assertEqual(w.getvalue(), "1234:\n")

    def test_print6 (self) :
        w = StringIO()
        netflix_print(w, "345345", 2.3)
        self.assertEqual(w.getvalue(), "2.3\n")

    # -----
    # solve
    # -----

    def test_solve1 (self) :
        r = StringIO("10035:\n1651047\n811486\n1727192")
        w = StringIO()
        netflix_solve(r, w)
        self.assertEqual(w.getvalue(), "10035:\n2.6\n4.7\n5.0\nRMSE: 0.83")

    def test_solve2 (self):
        read = StringIO("1016:\n687304")
        write = StringIO()
        netflix_solve(read, write)
        self.assertEqual(write.getvalue(), "1016:\n1.0\nRMSE: 0.72")

    def test_solve3 (self):
        reader = StringIO("10160:\n1495561\n1859181")
        writer = StringIO()
        netflix_solve(reader, writer)
        self.assertEqual(writer.getvalue(), "10160:\n3.0\n2.6\nRMSE: 1.16")

    # ----
    # main
    # ----

if __name__ == "__main__" :
    main()

