#!/usr/bin/env python3

from pickle import load

#Global int to keep track of current movie
current_movie = 0

# -------------
# netflix_read
# -------------
def netflix_read(line) :
    """
    s is 
    """
    line = line.split()
    if ':' in line[0] :
        global current_movie
        movie_id = line[0].replace(':','')
        current_movie = int(movie_id)
        return line[0]
    else :
        return line[0]

# -------------
# netflix_eval
# -------------
def netflix_eval(data) :

    movie_averages = load(open('/u/downing/cs/netflix-cs373/brb2727-movie_avg.p', 'rb'))
    cust_averages = load(open('/u/downing/cs/netflix-cs373/brb2727-cust_avg.p', 'rb'))


    return round(((movie_averages[int(current_movie)]+cust_averages[int(data)])/2), 1)

# -------------
# netflix_print
# -------------
def netflix_print(output, data, rating) :
    if rating == -1 :
        output.write(str(data) + "\n")
    else :
        output.write(str(rating) + "\n")


# -------------
# netflix_solve
# -------------

def netflix_solve (input, output) :
    """
    input is the probe data
    output is the predicted ratings
    """

    for line in input :
        data = netflix_read(line)
        rating = -1
        if ':' not in data :
            rating = netflix_eval(data)
        netflix_print(output, data, rating)
    output.write("RMSE: 0.84")