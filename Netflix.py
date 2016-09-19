#!/usr/bin/env python3

from pickle import load

#Global int to keep track of current movie
current_movie = 0

predicted_ratings = {}
current_movie_list = {}

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
        global current_movie_list
        movie_id = line[0].replace(':','')
        if current_movie_list:
            predicted_ratings[current_movie] = current_movie_list
        current_movie_list = {}
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
    total_average = 3.2281371945000967 #credit to Carlos for posting on piazza

    value = total_average + (movie_averages[int(current_movie)] - total_average)+(cust_averages[int(data)] - total_average)

    if value < 1 :
        return 1.0
    elif value > 5 :
        return 5.0
    else :
        return round(value, 1)

# -------------
# netflix_print
# -------------
def netflix_print(output, data, rating) :
    if rating == -1 :
        output.write(str(data) + "\n")
    else :
        output.write(str(rating) + "\n")

# -------------
# get_rmse
# -------------      
def get_rmse() :
    global predicted_ratings
    sum = 0
    count = 0
    actual_ratings = load(open('/u/downing/cs/netflix-cs373/cat3238-actual.p', 'rb'))
    for movie_id in predicted_ratings:
        for customer_id in predicted_ratings[movie_id]:
            predicted_rating = predicted_ratings[movie_id][customer_id]
            actual_rating = actual_ratings[movie_id][int(customer_id)]
            if actual_rating:
                sqr_err = (actual_rating - predicted_rating) **2
                sum += sqr_err
                count += 1
    avg = sum / count
    return avg ** 0.5

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
            global current_movie_list
            current_movie_list[data] = rating
        netflix_print(output, data, rating)
    global predicted_ratings
    predicted_ratings[current_movie] = current_movie_list
    RMSE = get_rmse()
    output.write("RMSE: "+ str(round(RMSE, 2)))