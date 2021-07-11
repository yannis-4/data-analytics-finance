import pandas as pd
import numpy as np
import os

# preparing names for later use
cwd = os.getcwd()
data_folder = os.path.join(cwd,"datasets/")
data_folder_files = os.listdir(data_folder)
main_folder_files = os.listdir(cwd)

#print(data_folder_files)
print("The files in %r: %s" % (cwd, main_folder_files))
print("The files in %r: %s" % (cwd, data_folder_files))
print("   ")

# preparing 3 lists for the below loop
merged_data = []
stocks_list = []
data_files = []

# beginning of the loop in order to merge all stocks datasets from the dataset folder
for x in data_folder_files:

    # trimming .csv
    y = x.replace(".csv", "")

    # adding the stock to the list
    stocks_list.append(y)

    # adding the data files to the list
    z = x.replace(".csv", "_data")
    data_files.append(z)

    # reading the csv in loop
    z = pd.read_csv(os.path.join(data_folder, x))

    # adding 1 column with the stock name
    z.insert(0, 'Stock', y, True)


    merged_data.append(z)  # end of the loop


# appending all datasets into one
appended_data = pd.concat(merged_data)



# check for missing or N/A values and print 2 reports
count_missing_values = appended_data.isnull().sum()
print('The below are the number of missing values', '\n', count_missing_values)

print("   ")

count_na_values = appended_data.isna().sum()
print('The below are the number of N/A values', '\n', count_na_values)

print("   ")


# setting up the check for NA lines and columns
drop_na_rows= appended_data.dropna()
# print the shape of the 2 datasets for comparison
print("Below you can compare the size of the 2 datasets")
print(appended_data.shape,drop_na_rows.shape)
print("   ")


print("After comparing the 2 datasets the results are:")
# if statement to see if there are missing values. If there missing they are filled with the most recent one.
if appended_data.shape == drop_na_rows.shape:
    cleaned_data = appended_data.fillna(method='bfill', axis=0).fillna(0)
    print('No lines were missing / dropped')
else:
    cleaned_data = appended_data
    print('All missing lines that were missing have been dropped')


print("   ")
print("   ")


# sorting the appended dataset by Date
appended_data.sort_values(by=['Date'], inplace=True)
#print(appended_data) # use this to check how the data looks



# reporting the size of the final dataset
print('The final merged dataset has this shape:', cleaned_data.shape)
print("   ")



# Some useful lists of the project
print("The stocks we examined are:")
print(stocks_list)
print("   ")
print("The individual dataset files are:")
print(data_files)