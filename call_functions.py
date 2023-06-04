import pandas as pd
from sqlalchemy import create_engine

#This function parses a .csv file into a list of Functions.
# This is a common function to process train, test and ideal file and converts them into a dataframe for further processing
#When iterated, it returns a function 
#The .csv file has its first column representing x-values and the subsequent columns represent y-values. 
#The csv_file parameter specifies the local path of the .csv file.

class eligible_function:
    
    def __init__(self, csv_file):
        self._functions = []

        try:    
            self._function_data = pd.read_csv(csv_file)
        except FileNotFoundError:
            print("Trouble reading the file {}".format(csv_file))
            raise

        #The x values are store in  column x_col 
        #The process involves iterating over each column within a pandas DataFrame and using the data to create a new Function object.
        x_col = self._function_data["x"]

        for name_of_column, data_of_column in self._function_data.iteritems():
            if "x" in name_of_column:
                continue
            # store  y colum and concat them 
            sub_y= pd.concat([x_col, data_of_column], axis=1)
            f = function.df_overwrite(name_of_column, sub_y)
            self._functions.append(f)

    
    #This function utilizes the pandas .to_sql() Func to write the data to a local SQLite database. 
    #If the file already exists, it will be replaced. The file_name parameter denotes the name of the database, 
    #and the append_name parameter adds a specific suffix to the original column names.
    #Additionally, write_process is created using SQLAlchemy, which automatically handles the creation of the database if it does not already exist.

    def write_sqlite(self, file):
               
        copy_data = self._function_data.copy()
        copy_data.columns = [name.capitalize() for name in copy_data.columns]
        copy_data.set_index(copy_data.columns[0], inplace=True)

        copy_data.to_sql(
            file,
            create_engine('sqlite:///{}.db'.format(file), echo=False),
            if_exists="replace",
            index=True,
        )

    @property
   
    #The function returns an object that contains a list of all the functions.
    #Additionally, the user has the option to iterate directly over the object itself.
    #The return type of the functions is an object.
    
    def functions(self):

        return self._functions

    def __iter__(self):
        
        return eligible_func_Iterator(self)

    def __repr__(self):
        return "Contains {} number of functions".format(len(self.functions))

#eligible_func_Iterator iterates eligible  function 
class eligible_func_Iterator():
    
    def __init__(self, eligible_function):
        #This simple class which handles the iteration over a eligible_function
        self._index = 0
        self._eligible_function = eligible_function
    
    # Iterates every function under eligible functions and returns a function object 

    def __next__(self):
        
        if self._index < len(self._eligible_function.functions):
            desired_val = self._eligible_function.functions[self._index]
            self._index = self._index + 1
            return desired_val
        raise StopIteration
        
#This object holds the X and Y values of a function and is implemented using a Pandas dataframe.
#It offers several handy functionalities that simplify regression calculations. 
#These include:
#Ability to assign a name to the function for future retrieval.
#Iterable nature where it returns a point represented as a dictionary.
#Capability to retrieve a Y-Value by providing an X-Value.
#Support for subtracting two functions, resulting in a dataframe that represents the deviation between them.

class function:       
    def __init__(self, name):
        self._name = name
        self.dataframe = pd.DataFrame()
        
    #Get Y value
  
    
  # use panda iloc functiontion to find the x and return the corresponding y
  # If it is not found, an exception is raised
    def y_placement_vs_x(self, x):       
       
        key_finder = self.dataframe["x"] == x
        try:
            return self.dataframe.loc[key_finder].iat[0, 1]
        except IndexError:
            raise IndexError

    @property
    #returns the name of the function as string
    def name(self):

        return self._name

    def __iter__(self):
        return iter_function(self)
   
    #This function returns a new dataframe after subtracting the value of 2 dataframes at hand 

    def __sub__(self, other):

        deviation = self.dataframe - other.dataframe
        return deviation

    @classmethod

    #Provided a dataframe where the original column names are overwritten to "x" and "y"
        
    def df_overwrite(cls, name, dataframe):
        
        function = cls(name)
        function.dataframe = dataframe
        function.dataframe.columns = ["x", "y"]
        return  function

    def __repr__(self):
        return "Function for {}".format(self.name)

# An ideal function encompasses the predictive function, training data, and regression information.
# When using it for classification purposes, you can provide a threshold_factor to set a threshold.
#If no threshold_factor is provided, it will default to the maximum deviation between the ideal and training functions.
class func_ideal(function):
    
    def __init__(self, function, tr_func, err):
        super().__init__(function.name)
        self.dataframe = function.dataframe

        self.tr_func = tr_func
        self.error = err
        self._threshold_value = 1
        self._threshold = 1
       
        # The two functions iterated go into this function  and substracted to get the difference 
        # From the resulting dataframe, it finds the one which is largest
    

    @property
    #This defines the acceptable threshold for the regression in order to be considered as a valid classification. 
    #While it is possible to directly set a threshold (useful for unit testing), it is generally recommended to provide a threshold_factor instead.
    #This function returns a The threshold value
       
    def threshold(self):
        
        self._threshold = self.threshold_factor * self.deviate_max
        return self._threshold

    @threshold.setter
    def threshold(self, value):

        self._threshold = value

    @property

    def threshold_factor(self):

        return self._threshold_value

    @threshold_factor.setter
    def threshold_factor(self, value):
        self._threshold_value = value

    @property
    # This function retrieves the maximum deviation between the classifying function and the training function it is derived from.
    # This function returns the maximum deviation

    def deviate_max(self):
       
        diff_df = self.tr_func - self
        diff_df["y"] = diff_df["y"].abs()
        deviate_max = max(diff_df["y"])
        return deviate_max


class iter_function:

    def __init__(self, function):
        self._function = function
        self._index = 0
    # When iterating over the functions, it returns a dictionary that gives the corresponding point."
    def __next__(self):

        if self._index < len(self._function.dataframe):
            desired_value_dict = (self._function.dataframe.iloc[self._index])
            pnt = {"x": desired_value_dict.x, "y": desired_value_dict.y}
            self._index += 1
            return pnt
        raise StopIteration
        
        
#Calculates the squared difference between the 2 functions 
#Sums all the deviations and gives te total deviation of the 2 combination functions at every iteration 
#facilitating minimize the sum of all y deviations squared 
 #The function returns an Ideal Function that is based on a training function and a list of ideal function combination
def least_squared(tr_func, eligible_func_list):
   
    least_deviate_func = None
    deviation_min= None
    for function in eligible_func_list:
        deviation = function - tr_func
        deviation["y"] = deviation["y"] ** 2
        sum_deviation = sum(deviation["y"])
        
        if ((deviation_min== None) or sum_deviation < deviation_min):
            deviation_min= sum_deviation
            least_deviate_func = function

    ideal_function = func_ideal(function=least_deviate_func, tr_func=tr_func, err=deviation_min)
    return ideal_function


#Returns points that fall within the threshold of a classification.
#A tuple is formed, consisting of the nearest classification, if any, and the distance between the functions.

def classify_func(pnt, ideal_funcs):

    min_func_temp= None
    min_dist_temp = None

    for function_ideal in ideal_funcs:
        try:
            point_y_curr = function_ideal.y_placement_vs_x(pnt["x"])
        except IndexError:
            print("This point is not in the classification function")
            raise IndexError

# Using Absolute distance to calculate the difference between the points
        dist = abs(point_y_curr - pnt["y"])

        if (abs(dist <  function_ideal.threshold)):

            # Returns the function with the lowest distance
            if ((min_func_temp== None) or (dist < min_dist_temp)):
                min_func_temp= function_ideal
                min_dist_temp = dist

    return min_func_temp, min_dist_temp
