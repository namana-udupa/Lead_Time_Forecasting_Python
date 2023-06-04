# -*- coding: utf-8 -*-
"""
Created on Sun May 28 19:44:51 2023

@author: Namana
"""

import math
from call_functions import eligible_function, least_squared, classify_func
#deviation_sqaured,
from visualize import generate_chart, plot_matched_points
from nsview import to_sqlite_deviate_data

# This constant is the threshold as per the assignment criterion.
#Calculation says: Existing maximum deviation of the calculated regression does not exceed #the largest deviation 
#between training dataset (A) and the ideal function (C) chosen for it by more than factor sqrt(2)
threshold = math.sqrt(2)

if __name__ == '__main__':
    
    # Assign the directory path where the csv files are present. 
    ideal_file = "C:\\Users\\Namana\\OneDrive\\Desktop\\IU MSDS Upgrad\\Python programming\\Python_Assignment\\dataset\\ideal.csv"
    train_file = "C:\\Users\\Namana\\OneDrive\Desktop\\IU MSDS Upgrad\\Python programming\\Python_Assignment\\dataset\\train.csv"

    # Pass the csv file path to the function eligible_function so that it reads the file and converts them into  dataframes
    # X and Y points will be stored and ready to be processed. 

    possible_ideal_functions = eligible_function(csv_file=ideal_file)
    training_func= eligible_function(csv_file=train_file)

    # the above created Dataframes are sent to the write_sqlite function that uses the .to_sql function 
    #to write the read data into DB
    possible_ideal_functions.write_sqlite(file="ideal_functions")
    training_func.write_sqlite(file="train_functions")
    
    # training_func  stores a total of four functions , possible_ideal_functions contains the 50 stored functions.
    # we can utilize this data to calculate an Ideal Function for each of the four training function
    #Store the best fitting function, the train data, and  compute the tolerance. 
    #Task involves iterating over all training_func assigned above and ideal functions 
    # and any matching ideal functions are saved in a list called  ideal_funcs
    ideal_funcs = []
    for train_func in training_func:
        # least_squared is able to compute the best fitting function given the train function bases on the calculation mentioned above 
        ideal_function = least_squared(tr_func=train_func, eligible_func_list=possible_ideal_functions.functions)

        ideal_function.threshold_factor = threshold
        ideal_funcs.append(ideal_function)

    #Plot the scatter graph with train functions vs ideal function w.r.t its squared error 
    generate_chart(ideal_funcs, "train_vs_ideal")


   # Leverage the  eligible_function, which offers the required functionalities to load a CSV file, thus reusing it. 
   #Unlike before, the  eligible_function will now contain a single "function" located at index [0]. 
   #The advantage of this setup is that we can iterate over each point using the function object.
    test_file = "C:\\Users\\Namana\\OneDrive\Desktop\\IU MSDS Upgrad\\Python programming\\Python_Assignment\\dataset\\test.csv"
    test_functions = eligible_function(csv_file=test_file)
    test_func= test_functions.functions[0]

    pnts_vs_ideal_function = []
    for pnt in test_func:
        ideal_func, Delta_Y = classify_func(pnt=pnt, ideal_funcs=ideal_funcs)
        output = {"pnt": pnt, "category": ideal_func, "Delta_Y": Delta_Y}
        pnts_vs_ideal_function.append(output)

    # A collection of dictionaries is contained within the variable "points_with_ideal_functions.
    #These dictionaries correspond to the classification outcomes of individual points.

    #  visualize all the points along with their respective classification functions.
    plot_matched_points(pnts_vs_ideal_function, "point_vs_ideal_function")

    # Ultimately, the dictionary object is employed to store the data in a SQLite database. 
    #To simplify the process and avoid dealing directly with SQL language, a MetaData object is utilized with a pure SQLAlchemy approach.
    to_sqlite_deviate_data(pnts_vs_ideal_function)
   
    print("The 3 Sqlite DB files and 2 html files are created:")
    print("training.db: 4 training functions - SQLITE DB")
    print("ideal.db: 50 ideal functions - SQLITE DB")
    print("data_structure.db: The outcome of the point test involves the computation of the ideal function and its corresponding delta.")
    print("train_and_ideal.html: Visualization- The training data is represented as scattered points, while the optimal fitting ideal function is depicted as a curve.")
    print("points_and_ideal.html:Visualization- Display the figure that shows the distance between the points that have a matching ideal function.")

    print("Author: Namana Udupa")
    print("Date: 01. June 2023")
    print("Job successfully completed")