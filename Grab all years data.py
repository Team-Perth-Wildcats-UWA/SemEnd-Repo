import requests
from bs4 import BeautifulSoup
import time
import xlwt
import xlrd
from xlutils.copy import copy
import pandas as pd

# set the search range for the last 10 years.
year = time.localtime().tm_year
year_range = 12
year_list = []
col = 0
row = 0

# Season - 12 options ---
# League - Australian NBL ---
# Team - All Australian NBL Teams ---
# Stat Type - Averages, Totals, Advanced Stats (3 options) ---
# Prospects - All Prospects  ---
# Position - PG, SG, SF, PF, C (5 options) ---
# Qualified - Un-ticked ---
# Pace Adjusted - Ticked ---

# in total, 12 x 3 x 5 options = 180 extractions.

# There should be 3 CSV files-for each Stat Type. Each CSV file will contain data for all 12 seasons, and all positions.

# Each table will have as many columns as shown in the website PLUS 2 columns - Season and Position

# Set the year list for the last 10 years
for k in range(year_range):
    reduceYear = year - k
    year_list.append(reduceYear)
print(year_list)

# set the Stat Type
stat_Type = ['Averages', 'Totals', 'Advanced_Stats', 'Per_Minute']

# set the position type:
position_Type = ['PG', 'SG', 'SF', 'PF', 'C']

new_data = []

player_data = []

# set the year web address list
player_year_data = [(2, 2012), (99, 2013), (191, 2014), (260, 2015), (345, 2016), (427, 2017), (516, 2018), (660, 2019),
                    (764, 2020), (865, 2021), (954, 2022), (1048, 2023), (1143, 2024)]

try_list = []


# set the new output Excel name
def set_xls_name(stat_type):
    # xls doc set
    book_name_xls = 'Data with All year ' + stat_type + '.xls'
    return book_name_xls


# set the new output excels sheet name
def set_sheet_name(split):
    sheet_name_xls = split
    return sheet_name_xls


# output the selected data into the new Excel doc
def write_excel_xls(path, sheet_name, value):
    index = len(value)  # Gets the number of rows to write data
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    for i in range(0, index):
        sheet.write(0, i, value[i])  # Write data (corresponding rows and columns) to a table
    workbook.save(path)
    print("Different Year, Team, Position Data and Data_Type Added.")


# read the new Excel file and get the existed rows in the sheet and add data
def write_excel_xls_append(path, value):
    index = len(value)
    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheet_names()  # Gets all the sheets in the workbook
    worksheet = workbook.sheet_by_name(sheets[0])  # Gets the first sheet
    rows_old = worksheet.nrows  # Get the existed rows in the sheet
    new_workbook = copy(workbook)  # Converts a copy of a xlrd object to a xlwt object
    new_worksheet = new_workbook.get_sheet(0)  # Gets the first sheet in the transformed workbook
    for i in range(0, index):
        for o in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, o, value[i][o])  # add data from i+rows_old lines
    new_workbook.save(path)
    print('Total lines is : ' + index.__str__())
    print("xls doc complete")


# output the selected data into the other new Excel doc (because the data type is diff from all year data)
def new_data_append(data_list, first_size, years, position):
    chunk_size = first_size
    empty_list = [years.__str__(), position.__str__()]
    for i in range(1, len(data_list), chunk_size):
        new_data.append(data_list[i:i + chunk_size - 1] + empty_list)
    return new_data


def new_player_data_append(data_list, first_size):
    chunk_size = first_size
    for i in range(0, len(data_list), chunk_size):
        player_data.append(data_list[i:i + chunk_size])
    return player_data


# grab each year player's data from website by for loop
def get_selected_data(y, z):
    for x in year_list:
        url = 'https://basketball.realgm.com/international/league/5/Australian-NBL/stats/{}/{}/All/All/points/{}' \
              '/desc/1?pace_adjustment='.format(x, y, z)
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        # get the data for head and each team
        table = content.find_all('table')
        head_list = []
        data_list = []

        # Find selected data by analysing html tags
        for t in table:
            h_list = t.find_all('th')
            tm_list = t.find_all('td')
            for u in tm_list:
                data_list.append(u.string)
            for h in h_list:
                head_list.append(h.string)

        first_size = head_list.__len__()
        head_list.pop(0)
        head_list.append('Season')
        head_list.append('Position')

        write_excel_xls(set_xls_name(y), set_sheet_name(y), head_list)

        # calculate each for loop new data list length
        new_data_append(data_list, first_size, x, z)

        print('successful add ' + x.__str__() + "'s" + ' Stat Type: ' + y + '. Split by: ' + z)
    return new_data


# grab all player's data from website by for loop
def get_player_data():
    for i in player_year_data:
        url = 'https://basketball.realgm.com/international/league/5/Australian-NBL/players/{}/{}'.format(i[0], i[1])
        print(i[0], i[1])
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        # get the data for head and each team
        table = content.find_all('table')
        head_list = []
        data_list = []
        # Find selected data by analysing html tags
        for t in table:
            h_list = t.find_all('th')
            tm_list = t.find_all('td')
            for u in tm_list:
                if u.string is None:
                    tem_list = u.find_all('a')
                    for z in tem_list:
                        try_list.append(z.text)
                    string1 = try_list[0] + ', ' + try_list[1]
                    data_list.append(string1)
                    try_list.clear()
                else:
                    data_list.append(u.text)
            for h in h_list:
                head_list.append(h.text)

        first_size = head_list.__len__()

        write_excel_xls(set_xls_name('All year Player_data'), set_sheet_name('Player_data'), head_list)

        # calculate each for loop new data list length
        new_player_data_append(data_list, first_size)

        print('successful add player data')
    return player_data


def delete_rows():
    filename = 'Data with All year Player_data.xls'
    df = pd.read_excel(filename)  # read excel all contents
    df1 = df.drop(['Pos'], axis=1)  # delete pos column
    df2 = df1.drop(['Team'], axis=1)  # delete pos column
    df2.to_csv('All year Player_data.csv', index=False)


# !!!!!if want to use different types of data, just change the tags below!!!!
# grab each year player data
for j in stat_Type:
    new_data.clear()
    for k in position_Type:
        write_excel_xls_append(set_xls_name(j), get_selected_data(j, k.__str__()))

# grab all year player data
write_excel_xls_append(set_xls_name('all year Player_data'), get_player_data())
delete_rows()
