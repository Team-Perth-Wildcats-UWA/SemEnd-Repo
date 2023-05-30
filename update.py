# test
import os
import time

import pandas as pd
import pymssql
import requests
import xlrd
import xlwt
from bs4 import BeautifulSoup
from xlutils.copy import copy
import numpy as np

# set default SettingWithCopyWarning in Pandas='None'
pd.options.mode.chained_assignment = None

# Connect the Wildcats database with local host SQL server
conn = pymssql.connect(host="127.0.0.1", user="lei", password="123456", database="Wildcats", charset="cp936")

if conn:
    print("Success connect the Wildcats database!")
else:
    print("Can not connect to the database plz find help!")
c1 = conn.cursor()
c2 = conn.cursor()
c3 = conn.cursor()
c4 = conn.cursor()

# set the search range for the last 10 years.
year = time.localtime().tm_year
year_list = [year]
print("This year is " + year_list[0].__str__())

col = 0
row = 0

# set the Stat Type
stat_Type = ['Averages', 'Totals', 'Advanced_Stats', 'Per_Minute']

# set the position type:
position_Type = ['PG', 'SG', 'SF', 'PF', 'C']

new_data = []


# set the new output Excel name
def set_xls_name(stat_type):
    # xls doc set
    book_name_xls = year.__str__() + ' New Data with ' + stat_type + '.xls'
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
    print("New Data updated.")


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


def new_data_append(data_list, first_size, years, position):
    chunk_size = first_size
    empty_list = [years.__str__(), position.__str__()]
    for i in range(1, len(data_list), chunk_size):
        new_data.append(data_list[i:i + chunk_size - 1] + empty_list)
    return new_data


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


# clear all the last updated data
def clear_last_update_data():
    remove1 = open('update_data.csv', "r+")
    remove2 = open('update_query.csv', "r+")
    remove1.truncate()
    remove2.truncate()


# find player id by match the name in SQL server
def find_player_id(name):
    sql1 = 'SELECT PlayerID FROM [dbo].[DimPlayer] WHERE Name = ' + " '" + name + "'"
    c1.execute(sql1)
    result = c1.fetchall()
    for x in result:
        return str(x[0])


# find a player team id by match the name in SQL server
def find_player_team_id(team):
    sql2 = 'SELECT TeamID FROM [dbo].[DimTeam] WHERE Team = ' + " '" + team + "'"
    c2.execute(sql2)
    result = c2.fetchall()
    for x in result:
        return str(x[0])


# find player position id by match the name in SQL server
def find_player_position_id(position):
    sql3 = 'SELECT PositionID FROM [dbo].[DimPosition] WHERE Position = ' + " '" + position + "'"
    c3.execute(sql3)
    result = c3.fetchall()
    for x in result:
        return str(x[0])


# select update date by query in SQL Table
def update_sql_query(player_id, value, header, excel):
    table_name = '[dbo].[Fact' + excel.replace('_', '') + ']'
    sql4 = 'UPDATE ' + table_name + ' SET [' + header[0] + '] = ' + str(value[0]) + ' WHERE PlayerID = ' + player_id
    c4.execute(sql4)
    conn.commit()
    print('Database has been updated')


# Read the new Excel doc and old excel doc by comparing each line to check if exist different data and output them into
# new csv files for user to check
def compare_data(excel):
    # read two excels
    excel_name1 = year.__str__() + ' Old Data with ' + excel.__str__() + '.xls'
    sheet_name1 = excel.__str__()
    excel_name2 = year.__str__() + ' New Data with ' + excel.__str__() + '.xls'
    sheet_name2 = excel.__str__()
    dt1 = pd.read_excel(excel_name1, sheet_name=sheet_name1)
    dt2 = pd.read_excel(excel_name2, sheet_name=sheet_name2)

    # confirm based compared row
    dt1_name = dt1['Player'].values.tolist()
    dt2_name = dt2['Player'].values.tolist()
    count = 0
    for i in dt1_name:
        if i in dt2_name:
            dt1_row = dt1.loc[dt1['Player'] == i]
            dt2_row = dt2.loc[dt2['Player'] == i]
            # compare two excels difference
            if dt1_row.equals(dt2_row):
                pass
            else:
                # count
                count += 1
                comparison_values = dt1_row.values == dt2_row.values
                rows, cols = np.where(comparison_values == False)

                data_type1 = ['Old']
                data_type2 = ['New']
                data_type3 = [excel]
                player_id = find_player_id(i)
                player_team_id = find_player_team_id((dt2_row['Team'].values.tolist())[0])
                player_position_id = find_player_position_id((dt2_row['Position'].values.tolist())[0])

                dt1_row['Data_Type'] = data_type3
                dt1_row['Data_Date'] = data_type1
                dt2_row['Data_Type'] = data_type3
                dt2_row['Data_Date'] = data_type2
                dt2_row['Player'] = player_id
                dt2_row['Team'] = player_team_id
                dt2_row['Position'] = player_position_id

                dt1_row.to_csv(r'update_data.csv', index=False, mode='a', header=True)
                dt2_row.to_csv(r'update_data.csv', index=False, mode='a', header=None)

                # separate the update data for a query
                del dt2_row['Data_Type']
                del dt2_row['Data_Date']
                dt2_row = dt2_row.rename(
                    {'Team': 'TeamID', 'Player': 'PlayerID', 'Position': 'PositionID', '3PM': '_3PM',
                     '3PA': '_3PA', '3P%': '_3P%'}, axis=1)
                # find match id in different data in SQL server
                different_value = dt2_row.iloc[rows, cols]
                different_header = different_value.keys().values.tolist()

                dt3 = dt2_row[['PlayerID']]
                dt3[different_header] = different_value
                dt3.to_csv(r'update_query.csv', index=False, mode='a', header=True)
                # print the details of what code found
                update_sql_query(player_id, (different_value.values.tolist())[0], different_header, excel)
                print("Find Player " + i + " has the different data in " + excel + " in " + year.__str__())
    if count == 0:
        print("Hi Dear user! There is nothing needs to update right now about " + excel + ", please update later. "
                                                                                          "Thanks")
    os.remove(excel_name1)
    os.rename(excel_name2, excel_name1)


# !!!!!if want to use different types of data, just change the tags below!!!!
# grab the new data from the RealGM website and save them into Excel files
clear_last_update_data()

for j in stat_Type:
    new_data.clear()
    for k in position_Type:
        write_excel_xls_append(set_xls_name(j), get_selected_data(j, k.__str__()))
    compare_data(j.__str__())
    conn.commit()

# close the connection to the database
c1.close()
c2.close()
c3.close()
c4.close()
conn.close()
