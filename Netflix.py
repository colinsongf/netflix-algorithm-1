#!/usr/bin/env python3

from pickle import load

#Global int to keep track of current movie
current_movie = 0

#Global dicts from caches
movie_averages = load(open('/u/downing/cs/netflix-cs373/brb2727-movie_avg.p', 'rb'))
cust_averages = load(open('/u/downing/cs/netflix-cs373/brb2727-cust_avg.p', 'rb'))

#Dict of our own predicted ratings
predicted_ratings = {}

# -------------
# netflix_read
# -------------
def netflix_read(line) :
    """
    line is the line in the input beiing read, either a movie or a customer 
    """
    line = line.split()
    if ':' in line[0] :         # if line represents a movie
        global current_movie
        movie_id = line[0].replace(':','')
        current_movie = int(movie_id) 
        return line[0]
    else :                      # otherwise, line represents customer
        return line[0]

# -------------
# netflix_eval
# -------------
def netflix_eval(data) :
    """
    data is the customer id
    """

    total_average = 3.7         # mean of all netflix ratings
    
    #Our prediction algorithm is the total average, plus the movie offset, plus the customer offset
    value = total_average + (movie_averages[int(current_movie)] - total_average)+(cust_averages[int(data)] - total_average)

    #make sure we don't make predictions greater than 5 or lower than 1
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
    """
    output is file being written to
    data is customer id or movie id
    rating is the predicted rating
    """
    if rating == -1 :           # if rating is -1, then this is a movie id
        output.write(str(data) + "\n")
    else :                      # else this is a customer id
        output.write(str(rating) + "\n")

# -------------
# get_rmse
# -------------      
def get_rmse() :
    global predicted_ratings
    sumval = 0
    count = 0
    
    #dict containing the actual ratings from netflix to compare against
    actual_ratings = load(open('/u/downing/cs/netflix-cs373/cat3238-actual.p', 'rb'))
    
    #for each movie in predicted ratings
    for movie_rating in predicted_ratings :
        
        #grab the rating to compare against
        actual_rating = actual_ratings[int(movie_rating[0])][int(movie_rating[1])]
        
        #grab our rating and evaluate
        predicted_rating = predicted_ratings[movie_rating]
        if actual_rating:
            sqr_err = (actual_rating - predicted_rating) **2
            sumval += sqr_err
            count += 1
    avg = sumval / count
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
        if ':' not in data : #if there's no colon, then the line represents a customer
            rating = netflix_eval(data)
            global predicted_ratings
            key = (current_movie, data)
            predicted_ratings[key] = rating
        netflix_print(output, data, rating)
    RMSE = get_rmse()
    output.write("RMSE: "+ str(round(RMSE, 2)))
