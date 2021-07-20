import pandas as pd
import numpy as np
import os
import requests
import json
import matplotlib.pyplot as plt

# just an introduction using a function
def my_function(yan):
    print("My name is " + yan + " and this is my project for UCD")
my_function("Yannis")

print("   ")

# preparing names for later use
cwd = os.getcwd()
data_folder = os.path.join(cwd,"datasets/")
data_folder_files = os.listdir(data_folder)
main_folder_files = os.listdir(cwd)

#print(data_folder_files)
print("The files in the home folder %r \nare: %s" % (cwd, main_folder_files))
print("   ")
print("The files in the data folder %r \nare: %s" % (data_folder, data_folder_files))
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

    # adding the dataset to the list
    merged_data.append(z)  # end of the loop


# appending all datasets into one
appended_data = pd.concat(merged_data)

print("All data files are now successfully merged in one dataset", '\n')

# check for missing or N/A values and print 2 reports
count_missing_values = appended_data.isnull().sum()
print('The below are the number of missing values','\n', count_missing_values)

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
print(appended_data) # use this to check how the data looks

# reporting the size of the final dataset
print('The final merged dataset has this shape:', cleaned_data.shape)
print("   ")

# Some useful lists of the project
print("The stocks we examined are:")
print(stocks_list)
print("   ")
print("The individual dataset files are:")
print(data_files)

print("   ")

# below we see the latest values for the MSFT stock with the use of an API
url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&&apikey=N5HP2RWWOV3JI4A5'
r = requests.get(url)
data = r.json()
print("Below is the most recent MSFT stock values:", '\n',json.dumps(data, indent = 4))

print("   ")

# this is a simple use of numpy creating an array out of a list
arr = np.array(stocks_list)
print("This is the shape of the initial array:", arr.shape)


# the below part of the code is all about graphs
# opening the 2 stocks csv that I will examine
msft = pd.read_csv(os.path.join(data_folder, 'MSFT.csv'))
aapl = pd.read_csv(os.path.join(data_folder, 'AAPL.csv'))

# keeping only 2 columns
msft_new = msft[['Date', 'Close']]
aapl_new = aapl[['Date', 'Close']]

# renaming the close column with the stock name
msft_new.columns = ['Date', 'MSFT']
aapl_new.columns = ['Date', 'AAPL']

# merging the 2 stocks into 1 dataset
two_stocks = pd.merge(msft_new, aapl_new)

# indexing the new dataset
stocks_indexed = (two_stocks.set_index('Date'))
print(stocks_indexed)

# dividing each row by the first row so that I can compare them easily setting the base in day 1
stocks_indexed_a = stocks_indexed / stocks_indexed.iloc[0]

# preparing the 1st graph that compares the 2
plt.figure(1)
for i, col in enumerate(stocks_indexed_a.columns):
    stocks_indexed_a[col].plot()
plt.title('MSFT and AAPL price comparison')
plt.xticks(rotation=70)
plt.legend(stocks_indexed_a.columns)

# exporting the plot as an image
plt.savefig('msft_vs_aapl_1.png', bbox_inches='tight')


# doing the exact same as above but only for the last year

# keeping the last year of data, then reseting the indexing
two_stocks_1y = two_stocks.drop(two_stocks.index[:-253])
two_stocks_1y = two_stocks_1y.reset_index(drop=True)
two_stocks_1y_indexed = (two_stocks_1y.set_index('Date'))
# dividing each row by the first row so that I can compare them easily setting the base in day 1
one_year_indexed = two_stocks_1y_indexed / two_stocks_1y_indexed.iloc[0]
# preparing the 2nd graph that compares the 2 (1 year data)
plt.figure(2)
for i, col in enumerate(one_year_indexed.columns):
    one_year_indexed[col].plot()
plt.title('MSFT and AAPL price comparison for last year')
plt.xticks(rotation=70)
plt.legend(one_year_indexed.columns)

# exporting the plot as an image
plt.savefig('msft_vs_aapl_2.png', bbox_inches='tight')




# third graph is about the volume traded in millions:
# adding a new column with the Trade value in millions for the 2 stocks
msft['Trade value in mln'] = msft['Volume'] * msft['Close'] / 1000000
aapl['Trade value in mln'] = aapl['Volume'] * aapl['Close'] / 1000000

# keeping only 2 columns
msft_volumes = msft[['Date', 'Trade value in mln']]
aapl_volumes = aapl[['Date', 'Trade value in mln']]

# renaming the close column with the stock name
msft_volumes.columns = ['Date', 'MSFT']
aapl_volumes.columns = ['Date', 'AAPL']

# merging the 2 stocks into 1 dataset
two_stocks_volumes = pd.merge(msft_volumes, aapl_volumes)
# deleting the Date column so that I only have the 2 volumes
del two_stocks_volumes['Date']

plt.figure(3)
plt.ylabel('')
two_stocks_volumes[two_stocks_volumes.columns[0:]].sum().plot.pie()
#pylab.ylabel('')
plt.title('MSFT and AAPL traded volumes in mln comparison')
plt.legend(two_stocks_volumes.columns)
plt.savefig('pie.png', bbox_inches='tight')
