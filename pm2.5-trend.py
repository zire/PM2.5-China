import csv
import os

# Define project-level variables

INPUT_FILES = [
'Shanghai_2011_HourlyPM25_created20140423.csv',
'Shanghai_2012_HourlyPM25_created20140423.csv',
'Shanghai_2013_HourlyPM25_created20140423.csv',
'Shanghai_2014_HourlyPM25_created20150203.csv',
'Shanghai_2015_HourlyPM25_created20160201.csv',
'Shanghai_2016_HourlyPM25_created20170201.csv',
'Shanghai_2017_HourlyPM25_created20170301.csv'
]
OUTPUT_FILE = 'shanghai-pm2.5-data-2011-2017.csv'
HEADINGS = ['Date(LST)', 'Hour', 'PM2.5 Value']
MEASURE_TIME = '15' # 12:00 at noon
FIRST_ROW_NUM = 3 # which row does the data set start

# Define script-level variables

class BCOLORS:
    RED         = '\033[91m'
    GREEN       = '\033[92m'
    YELLOW      = '\033[93m'
    BLUE        = '\033[94m'
    PURPLE      = '\033[95m'
    CYAN        = '\033[96m'
    GRAY        = '\033[97m'
    BLACK       = '\033[98m'
    ENDC        = '\033[0m'
    UNDERLINE   = '\033[4m'

# create empty list
data_clean = []

for input_file in INPUT_FILES:
    # Process input files

    f = open(input_file, 'rb')
    reader = csv.reader(f)

    # get field names from the correct row
    for i, row in enumerate(reader):
        if i == FIRST_ROW_NUM:
            headings_raw = row
            break

    # get meta info from input file
    data_raw = list(reader)
    row_count_raw = len(data_raw)
    col_count_raw = len(data_raw[0])
    file_size_raw = os.stat(input_file).st_size

    print("\n\tInput file " + BCOLORS.GREEN + input_file +BCOLORS.ENDC + " has " + BCOLORS.YELLOW + str(row_count_raw) + BCOLORS.ENDC + " rows" + " and " + BCOLORS.YELLOW + str(col_count_raw) + BCOLORS.ENDC + " columns in " + BCOLORS.YELLOW + str(file_size_raw) + BCOLORS.ENDC + " bytes.")

    for row in data_raw:
        hour = row[2][row[2].index(":")-2:row[2].index(":")]
        # filter out rows by only selecting measurements at the specified hour
        if hour == MEASURE_TIME:
            # filter out columns except date, hour and pm2.5 value
            data_clean.append([row[2][:10], hour, row[7]])

    # Create output files
    writer = csv.writer(open(OUTPUT_FILE, 'w'))

    writer.writerow(HEADINGS)
    for row in data_clean:
        writer.writerow(row)

    row_count_clean = len(data_clean)
    col_count_clean = len(data_clean[0])
    file_size_clean = os.stat(OUTPUT_FILE).st_size

    print("\n\tOutput file " + BCOLORS.BLUE + OUTPUT_FILE + BCOLORS.ENDC + " is created with " + BCOLORS.YELLOW + str(row_count_clean) + BCOLORS.ENDC + " rows" + " and " + BCOLORS.YELLOW + str(col_count_clean) + BCOLORS.ENDC + " columns in " + BCOLORS.YELLOW + str(file_size_clean) + BCOLORS.ENDC + " bytes.")
    print("\n")
