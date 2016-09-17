#!/usr/bin/env python3

import Pickle


# -------------
# netflix_read
# -------------
def netflix_read(s) :
	"""
	s is 
	"""


# -------------
# netflix_eval
# -------------
def netflix_eval() :

# -------------
# netflix_print
# -------------
def netflix_print() :


# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    r a reader
    w a writer
    """
    for s in r :
        i, j = netflix_read(s)
        v    = netflix_eval(i, j)
        netflix_print(w, i, j, v)