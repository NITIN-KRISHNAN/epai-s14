# epai-s14 Context Manager
 
## FUNCTIONS
    find_largest_car_maker()
        Function to find the largest car maker for each gender
        :return: dict of key= gender and values= list of car maker with maximum records
    
    form_all_info(line1, line2, line3, line4, min_last_updated_date=None) -> info.Info
        Function to convert list of values from csv to Info namedtuple
        :param line1: the list of values for each row of personal info csv
        :param line2: the list of values for each row of employment csv
        :param line3: the list of values for each row of vehicle csv
        :param line4: the list of values for each row of update status csv
        :param min_last_updated_date: min date above which records are current
        :return: Info named tuple
    
    form_employment_info(line: list) -> info.Employment
        Function to convert list of values from csv to Employment namedtuple
        :param line: the list of values for each row of the employment csv
        :return: Employment named tuple
    
    form_personal_info(line: list) -> info.PersonalInfo
        Function to convert list of values from csv to PersonalInfo namedtuple
        :param line: the list of values for each row of the personal_info csv
        :return: PersonalInfo named tuple
    
    form_update_status_info(line) -> info.UpdateStatus
        Function to convert list of values from csv to UpdateStatus namedtuple
        :param line: the list of values for each row of the update_status csv
        :return: UpdateStatus named tuple
    
    form_vehicles_info(line: list) -> info.Vehicle
        Function to convert list of values from csv to Vehicle namedtuple
        :param line: the list of values for each row of the vehicles csv
        :return: Vehicle named tuple
    
    read_file_gen(file_name)
        Generator to read the given csv file, where each ticket row is returned as a corresponding NamedTuple
        :return: Generator to read the parking tickets csv file
    
    read_file_gen_all(min_last_updated_date=None)
        generator function to give single iterable that combines all the columns from all the iterators
        :param min_last_updated_date: min date above which records are current
        :return: generator to read entry from all csv and combine into one Info named tuple
    
    read_file_gen_all_fresh()
        reads current records whose last updated time is greater than or equal to 2017-01-03
        :return: generator to read current records

## DATA
    EMPLOYMENT_FILE_NAME = 'assignment/employment.csv'
    PERSONAL_INFO_FILE_NAME = 'assignment/personal_info.csv'
    UPDATE_STATUS_FILE_NAME = 'assignment/update_status.csv'
    VEHICLES_FILE_NAME = 'assignment/vehicles.csv'

## [Test Jupyter notebook](test.ipynb) contains usage of functions