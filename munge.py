# open raw data
import os
import csv

platform_agnostic_file_path = os.path.join('data', '2322814_ALL_LATEST.csv', )
csv_reader = csv.DictReader(open(platform_agnostic_file_path, 'r', encoding="utf-8-sig"))

data = list(csv_reader)


# define a function to figure out whether the column have same value
def check_values_for_key(dicts, key, value):
    count = 0
    for d in dicts:
        if key in d and d[key] == value:
            count += 1
    if count == len(data):
        return True

# build a list to store all possible values and keys
key_to_check = []
value_to_check = []
for key,value in data[0].items():
    key_to_check += [key]
    value_to_check += [value]

# if the columns have the same value for all data, we will delete the columns
key_to_delete = []
for i in range(len(key_to_check)):
    if check_values_for_key(data, key_to_check[i], value_to_check[i]) == True:
        key_to_delete += [key_to_check[i]]


for element in data:
    for key in key_to_delete:
        if key in element:
            del element[key]


new_data = []
for element in data:
    # change column name to more specific one according to deleted column
    new_element = {}
    for key,value in element.items():
        if key == 'DIM_TIME':
            new_element[key + ' (Year)'] = value
        elif key == 'VALUE_NUMERIC' or key == 'VALUE_NUMERIC_LOWER' or key == 'VALUE_NUMERIC_UPPER':
            
            # change numerical value into percentage 
            new_element[key + ' (%)'] = format(float(value)/10, '.2f')
        else:
            new_element[key] = value

        # Find whether there are typical missing value in data
        if (str.upper(value) in ['NAN', 'NONE', 'NULL']) or (value in ['~', '']):
            print('There are missing value')
     
    new_data.append(new_element)

# Find how how many years in our data and "who are them"
time_list = []

for element in new_data:
    if element['DIM_TIME (Year)'] not in time_list:
        time_list += [element['DIM_TIME (Year)']]

counter_dic = {}

# Find from which year the country data is complete
for year in time_list:
    counter = 0  
    for element in new_data:
            
        if (year in element.values()) and element['DIM_SEX'] == 'Total':
            counter += 1
        counter_dic[year] = counter
print(counter_dic)
 

# Define the folder where the CSV file will be saved
data_folder = 'data'
# Define the CSV file name
csv_filename = 'clean_data.csv'

# Create the data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Write the list of dictionaries to a CSV file in the data folder
with open(os.path.join(data_folder, csv_filename), mode='w', newline='', encoding="utf-8-sig") as file:
    # Create a DictWriter object with fieldnames set to the keys of the first dictionary in the list
    writer = csv.DictWriter(file, fieldnames=new_data[0].keys())
    
    # Write the header
    writer.writeheader()
    
    # Write the data rows
    for row in new_data:
        writer.writerow(row)