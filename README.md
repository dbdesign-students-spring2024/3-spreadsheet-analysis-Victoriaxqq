# Spreadsheet Analysis

## Data set Details
### Data finding
We got the dataset from the World Health Organization's (WHO) website. The dataset includes the mortality rate under 5 years old(per 1000 births) with different countries, different years, and different genders. [Here](https://data.who.int/indicators/i/2322814) is the link to the URL of our data source. And we downloaded the original dataset in **CSV** format.

Here are the first 11 rows (including header row) of our raw data:

| IND_UUID  | IND_NAME | IND_CODE | DIM_GEO_CODE_M49 |GEO_NAME_SHORT | DIM_TIME  | DIM_TIME_TYPE | DIM_SEX   | DIM_VALUE_TYPE | VALUE_NUMERIC | VALUE_NUMERIC_LOWER | VALUE_NUMERIC_UPPER | DIM_PUBLISH_STATE_CODE |
|---------|---------------|---------|------|------| ----- | -----|------|-------|---------|----------|-------|------|
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 288 | Ghana | 1932 | YEAR | Total | RATE_PER_1000 | 364.84801 | 274.96307 | 487.53546 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 288 | Ghana | 1933 | YEAR | Total | RATE_PER_1000 | 357.97217 | 280.91705 | 458.23299 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 76 | Brazil | 1934 | YEAR | Total | RATE_PER_1000 | 266.51389 | 195.85071 | 364.17253 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 288 | Ghana | 1934 | YEAR | Total | RATE_PER_1000 | 351.63443 | 285.97236 | 433.59827 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 76 | Brazil | 1935 | YEAR | Total | RATE_PER_1000 | 263.67358 | 202.1598 | 343.61783 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 288 | Ghana | 1935 | YEAR | Total | RATE_PER_1000 | 345.45748 | 288.74483 | 414.04994 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 76 | Brazil | 1936 | YEAR | Total | RATE_PER_1000 | 260.95494 | 208.39146 | 326.18258 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 288 | Ghana | 1936 | YEAR | Total | RATE_PER_1000 | 338.58498 | 289.34532 | 397.67158 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 76 | Brazil | 1937 | YEAR | Total | RATE_PER_1000 | 258.43639 | 212.53268 | 313.24844 | PUBLISHED |
| 2322814 | Mortality rate (under 5) | MDG_0000000007 | 288 | Ghana | 1937 | YEAR | Total | RATE_PER_1000 | 332.59424 | 288.08474 | 384.23813 | PUBLISHED |



### Data munging
Firstly, when we get the data first, we found that there are several columns which may exactly the same for each row. For example, the first column is called “IND_UUID” which means indicator unique identifier. All rows (we superficially see) in this column are “2322814”. The second column is called “IND_NAME” which represents the name of the data in short. All rows (we superficially see) are “mortality rate (under 5)”. The third column is “IND_CODE” which means indicator codes. All rows (we superficially see) are “MDG_0000000007”. The problem is that these columns have relatively insignificant meaning for analysis.

To handle this problem, we decided to incorporate the (important) meaning of these columns into more significant columns and then remove them from the dataset. Firstly, we define a function `check_values_for_key` to search whether all data in one column is the same to prove our assumption: there are several columns which may exactly the same for each row. 
```
def check_values_for_key(dicts, key, value):
    count = 0
    for d in dicts:
        if key in d and d[key] == value:
            count += 1
    if count == len(data):
        return True
```
Then, we employed a loop to find out the columns which need to be deleted and set up a new list which excludes these columns. However, there are some "repeated" columns which are still useful for our analysis. For example, the seventh column is “DIM_TIME_TYPE” which indicates the units of the numerical data in the previous column. All rows are “YEAR”. In order to keep the usage of the column, we add the unit “year” to the header of the sixth column. In addition, the ninth column is “DIM_VALUE_TYPE” which indicates the units of the numerical data in the subsequent columns. All rows are “RATE_PER_1000”. For better analysis, we decided to change the numerical data in the tenth, the eleventh, and the twelfth columns into percentages by dividing 10.
```
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
```
After that, we actualized the change of columns header and values that we planed above.

Since the description in the website did not mention the format of missing values, we tried to search missing values with several of the most common formats, such as blank, “NaN”, and “None” in Python. 
```
# Find whether there are typical missing value in data
        if (str.upper(value) in ['NAN', 'NONE', 'NULL']) or (value in ['~', '']):
            print('There are missing value')
```
There isn't any output, so we did not find missing values.

The next problem we met is that we found that in some years the dataset does not contain every country which ever appears in the dataset, which has a negative influence on calculating the average of each country per one year. For example, the dataset of 1932 only contains the death rate of one country, Ghana. Therefore, we developed coding to search which year includes the complete countries. 
```
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
```
As the result, the output is a dictionary which key represents year and values represents how many countries included. We found that from 1990 to 2021, the data is completed (206). Then, we decided to remove all years with countries missing. We processed the dataset in a spreadsheet Excel. Firstly, we set an indicator to determine whether the year is greater than 1990 or not. If the year is greater, we generate “keep” in another column as the indicator. If the year is smaller than 1990, we generate “delete” in the column. By automatic filter, only “delete” becomes visible in the dataset. Then, we choose all visible rows and delete them. In that case, we can clean the dataset. 

Here is our [original raw data](file: /Users/apple/Desktop/spreadsheet/3-spreadsheet-analysis-Ruojin-song/data/2322814_ALL_LATEST.csv)
, munged data, and the spreadsheet.

## Analysis