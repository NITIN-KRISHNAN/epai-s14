from datetime import datetime
from collections import namedtuple
import csv
from collections import OrderedDict

PERSONAL_INFO_FILE_NAME = "assignment/personal_info.csv"
EMPLOYMENT_FILE_NAME = "assignment/employment.csv"
VEHICLES_FILE_NAME = "assignment/vehicles.csv"
UPDATE_STATUS_FILE_NAME = "assignment/update_status.csv"


PersonalInfo = namedtuple("PersonalInfo", "ssn, first_name, last_name, gender, language")
Employment = namedtuple("Employment", "employer, department, employee_id, ssn")
UpdateStatus = namedtuple("UpdateStatus", "ssn, last_updated, created")
Vehicle = namedtuple("Vehicle", "ssn, vehicle_make, vehicle_model, model_year")
Info = namedtuple("Info", list(OrderedDict.fromkeys(PersonalInfo._fields + Employment._fields + Vehicle._fields +
                                                    UpdateStatus._fields)))


def form_personal_info(line: list) -> PersonalInfo:
    """
    Function to convert list of values from csv to PersonalInfo namedtuple
    :param line: the list of values for each row of the personal_info csv
    :return: PersonalInfo named tuple
    """
    ssn = line[0]
    first_name = line[1]
    last_name = line[2]
    gender = line[3]
    language = line[4]
    personal_info = PersonalInfo(ssn, first_name, last_name, gender, language)
    return personal_info


def form_employment_info(line: list) -> Employment:
    """
    Function to convert list of values from csv to Employment namedtuple
    :param line: the list of values for each row of the employment csv
    :return: Employment named tuple
    """
    employer = line[0]
    department = line[1]
    employee_id = line[2]
    ssn = line[3]
    employment_info = Employment(employer, department, employee_id, ssn)
    # print(employment_info)
    return employment_info


def form_vehicles_info(line: list) -> Vehicle:
    """
    Function to convert list of values from csv to Vehicle namedtuple
    :param line: the list of values for each row of the vehicles csv
    :return: Vehicle named tuple
    """
    ssn = line[0]
    vehicle_make = line[1]
    vehicle_model = line[2]
    model_year = int(line[3])
    vehicle = Vehicle(ssn, vehicle_make, vehicle_model, model_year)
    # print(vehicle)
    return vehicle


def form_update_status_info(line) -> UpdateStatus:
    """
    Function to convert list of values from csv to UpdateStatus namedtuple
    :param line: the list of values for each row of the update_status csv
    :return: UpdateStatus named tuple
    """
    ssn = line[0]
    last_updated = datetime.strptime(line[1], "%Y-%m-%dT%H:%M:%SZ")
    created = datetime.strptime(line[2], "%Y-%m-%dT%H:%M:%SZ")
    update_status = UpdateStatus(ssn, last_updated, created)
    # print(update_status)
    return update_status


def form_all_info(line1, line2, line3, line4, min_last_updated_date=None) -> Info:
    """
    Function to convert list of values from csv to Info namedtuple
    :param line1: the list of values for each row of personal info csv
    :param line2: the list of values for each row of employment csv
    :param line3: the list of values for each row of vehicle csv
    :param line4: the list of values for each row of update status csv
    :param min_last_updated_date: min date above which records are current
    :return: Info named tuple
    """
    personal_info = form_personal_info(line1)
    employment_info = form_employment_info(line2)
    update_status_info = form_update_status_info(line3)
    vehicle_info = form_vehicles_info(line4)
    if personal_info.ssn == employment_info.ssn == update_status_info.ssn == vehicle_info.ssn:
        personal_info_list = list(personal_info)
        employment_info_list = list(employment_info)
        employment_info_list.pop(3)
        update_status_info_list = list(update_status_info)
        update_status_info_list.pop(0)
        vehicle_info_list = list(vehicle_info)
        vehicle_info_list.pop(0)
        info = Info(*personal_info_list, *employment_info_list,  *vehicle_info_list, *update_status_info_list)
        # print(info)
        if min_last_updated_date:
            if getattr(info, 'last_updated') >= min_last_updated_date:
                return info
            else:
                print(info, "stale")
        else:
            return info
    else:
        raise ValueError("SSN do not match")


def read_file_gen(file_name):
    """
    Generator to read the given csv file, where each ticket row is returned as a corresponding NamedTuple
    :return: Generator to read the parking tickets csv file
    """
    line_num = 0
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            # skip first row as it contains headers
            if line_num == 0:
                line_num += 1
            else:
                if file_name == EMPLOYMENT_FILE_NAME:
                    yield form_employment_info(line)
                elif file_name == PERSONAL_INFO_FILE_NAME:
                    yield form_personal_info(line)
                elif file_name == VEHICLES_FILE_NAME:
                    yield form_vehicles_info(line)
                elif file_name == UPDATE_STATUS_FILE_NAME:
                    yield form_update_status_info(line)
                else:
                    raise ValueError("File name not supported")


def read_file_gen_all(min_last_updated_date=None):
    """
    generator function to give single iterable that combines all the columns from all the iterators
    :param min_last_updated_date: min date above which records are current
    :return: generator to read entry from all csv and combine into one Info named tuple
    """
    with open(EMPLOYMENT_FILE_NAME) as employment_file, open(PERSONAL_INFO_FILE_NAME) as personal_file, \
            open(UPDATE_STATUS_FILE_NAME) as update_status_file, open(VEHICLES_FILE_NAME) as vehicle_file:
        line_num = 0
        employment_csv_reader = csv.reader(employment_file, delimiter=',')
        personal_csv_reader = csv.reader(personal_file, delimiter=',')
        update_status_csv_reader = csv.reader(update_status_file, delimiter=',')
        vehicle_csv_reader = csv.reader(vehicle_file, delimiter=',')
        for (line1, line2, line3, line4) in zip(personal_csv_reader, employment_csv_reader,
                                                update_status_csv_reader, vehicle_csv_reader):
            if line_num == 0:
                line_num += 1
            else:
                info = form_all_info(line1, line2, line3, line4, min_last_updated_date=min_last_updated_date)
                if info:
                    yield info


def read_file_gen_all_fresh():
    """
    reads current records whose last updated time is greater than or equal to 2017-01-03
    :return: generator to read current records
    """
    return read_file_gen_all(min_last_updated_date=datetime(2017, 1, 3))


def find_largest_car_maker():
    """
    Function to find the largest car maker for each gender
    :return: dict of key= gender and values= list of car maker with maximum records
    """
    gen = read_file_gen_all()
    make_count_stats = dict()
    for entry in gen:
        gender = getattr(entry, "gender")
        vehicle_make = getattr(entry, "vehicle_make")
        make_count_for_gender = make_count_stats.get(gender, dict())
        make_count = make_count_for_gender.get(vehicle_make, 0)
        make_count += 1
        make_count_for_gender.update({vehicle_make: make_count})
        make_count_stats.update({gender: make_count_for_gender})
    # print(make_count_stats)

    res = dict()
    for item in make_count_stats.items():
        max_value = max(list(item[1].values()))
        # print(item[0], max_value)
        max_vehicles = [x[0] for x in item[1].items() if x[1] == max_value]
        # print(item[0],max_vehicles)
        res.update({item[0]: max_vehicles})
    # print(res)
    return res
