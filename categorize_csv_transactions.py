import csv
import datetime
from time import strftime
import os

print("This script will categorize transactions for a specific month...")

# log file detail
log_all = True
# console print detail
print_all = False

###########################
# Categories
###########################
csvfilename = "categories.csv"

if not (os.path.exists(csvfilename)):
    print(csvfilename + " does not exist")
    exit()


# all categories
categories_dictionary = {}
category_amount_dictionary = {}

# reading csv file
with open(csvfilename, 'r') as csvfile:
    # create a CSV reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
    categories = next(csvreader)

    # Iterate through each row in the CSV file
    for row in csvreader:
        i = 0
        for col in row:
            col_upper = col.upper()
            categories_dictionary[col_upper] = categories[i]
            category_amount_dictionary[categories[i]] = 0
            i += 1

    if print_all:
        for key, value in categories_dictionary.items():
            print(key + ": "+ value)

# creating the date object of today's date 
todays_date = datetime.date.today()

###########################
# User input
###########################
# get year
try:
    output_prompt = "Enter year (ex: " + str(todays_date.year) + "): "
    year = int(input(output_prompt))
except:
    print("Not a valid year")
    exit()

# verify intput
current_year = todays_date.year
if year < 1999 or \
   year > current_year:
    print("Not a valid year")
    exit()

# get month
try:
    output_prompt = "Enter month (ex: " + str(todays_date.month) + "): "
    month = int(input(output_prompt))
except:
    print("Not a valid month")
    exit()

# verify intput
if month < 1 or \
   month > 12:
    print("Not a valid month")
    exit()

# date
date_prefix = str(year) + "-" + "{:02d}".format(month)
if not (os.path.exists(date_prefix)):
    print("Folder " + date_prefix + " does not exist")
    exit()

# csv files
csv_folder = date_prefix + "/" + "csv_transactions"
if not (os.path.exists(csv_folder)):
    print("Folder " + csv_folder + " does not exist")
    exit()

# log file
log_folder = date_prefix + "/" + "logs"
if not (os.path.exists(log_folder)):
    os.mkdir(log_folder)

logfilename = date_prefix + "/" + "logs/{}_categorized.log".format(strftime('%Y-%m-%d__%H-%M-%S'))
f = open(logfilename, "w")

################################################
# Function to add transaction cost to category
################################################
def add_up_category_costs(category, price):
    if category in category_amount_dictionary:
        category_amount_dictionary[category] += price
    else:
        category_amount_dictionary[category] = price

##########################################
# Function to categorize transactions
##########################################
def categorize_transaction(info, price):
    for key in categories_dictionary:
        if len(key) >= 2:
            if key in info.upper():
                transaction_category = categories_dictionary[key]
                add_up_category_costs(transaction_category, price)
                break
    return categories_dictionary[key]

# all transactions list
transactions_list = []

###########################
# Go through CSV files
###########################
for csvfilename in os.listdir(csv_folder):
    if csvfilename.endswith(".csv"):
        csvfilepath = csv_folder + "/" + csvfilename

        # reading csv file
        with open(csvfilepath, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)

            # extracting fields in first row
            fields = next(csvreader)
            date_index = 0
            description_index = 1
            amount_index = 2

            if ("DATE" in fields[date_index].upper() and
                "AMOUNT" in fields[amount_index].upper()):
                # extracting each row one by one
                for row in csvreader:
                    if len(row) >= amount_index:
                        if len(row[0]) > 2:
                            date = row[date_index]
                            details = row[description_index]
                            amount = float(row[amount_index])

                            category = categorize_transaction(details, amount)

                            transaction = (csvfilename, date, details, category, amount)
                            transactions_list.append(transaction)


##############################
# Print out all transactions
##############################
if log_all:
    for transaction in transactions_list:
        f.write(str(transaction) + "\n")
    f.write("\n")

######################################
# Print out categories alphabetically
######################################
sorted_category_amount_dictionary = dict(sorted(category_amount_dictionary.items()))

for key, value in sorted_category_amount_dictionary.items():
    f.write(key + "," + format(value, '.2f') + "\n")

f.close()