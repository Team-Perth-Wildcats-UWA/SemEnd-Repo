import datetime
import requests
from bs4 import BeautifulSoup
import os
from datetime import date
import re
import pandas as pd

# set the search range for the last 10 years.
img_data = []

player_data = []

# set each season year web address to the list
season = ["34173", "30249", "27725", "24346", "21029", "18527", "9224", "2254", "934", "527", "525", "522", "521",
          "520"]

player_list = []

today = date.today()


# Grab the player information from each player's page url and grab the data of birthday.
# Then calculate the age.
# (Test if this player exists in the database first)
# (Test if this player's information page is available and if this player has his photos)
def get_player_url_date(url):
    res = requests.get(url).text
    content = BeautifulSoup(res, "html.parser")
    # get the data for head and each team
    main = content.find_all('main')
    for m in main:

        check = m.find('div', class_="row flex flex-wrap py-3 border-b border-gray-accent-200 text-sm")

        if check is not None:
            img = m.find('div', class_="mt-12 block lg:h-120 w-1/2 lg:w-full lg:absolute h-full bg-full-h-auto bg-top "
                                       "bg-no-repeat")
            img_url = img['style'].replace('background-image:', '').replace('url(', '').replace(')', '').replace('?;',
                                                                                                                 '')
            if img_url == "/images/person-placeholder.svg":
                img_url = "https://nbl.com.au/images/person-placeholder.svg"
            check_birthday = m.find('div', class_="w-1/3 text-gray-accent-500")

            if check_birthday.text.strip() == "Date of Birth":
                for div in check.find('div', class_="w-2/3 font-bold pl-5"):
                    divs = div.text.strip().replace(',', '').split()
                    day = re.findall(r"\d+", divs[0])
                    day = day[0]
                    month = divs[1]
                    year = divs[2]
                    b = day + '/' + month + '/' + year
                    b1 = datetime.datetime.strptime(b, "%d/%B/%Y").date()
                    age = today.year - b1.year - ((today.month, today.day) < (b1.month, b1.day))
                    return img_url, age
            else:
                return img_url, 'Unknown'
        else:
            return 'https://nbl.com.au/images/person-placeholder.svg', 'Unknown'


# get each team's player's information page url and send the new request by get_player_url_date(url) method
def get_selected_data(csv):
    csv_name = csv + '.csv'
    dt = pd.read_csv(csv_name)
    dt_name = dt['Player'].values.tolist()

    for x in season:
        url = 'https://nbl.com.au/stats/all-time?season={}'.format(x)
        print(url)
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        # get the data for head and each team
        main = content.find_all('main')

        # Find selected data by analysing html tags
        for m in main:
            for a in m.find_all('a', class_="flex-1 leading-none text-sm lg:text-base font-proxima-bold font-bold "
                                            "align-middle py-3 px-3"):
                href = a['href']
                player = a.text.strip()
                if player not in player_list:
                    if player in dt_name:
                        os.remove(csv_name)
                        index = dt[dt['Player'] == player].index.values
                        print(index)

                        player_list.append(player)
                        full_url = ('https://nbl.com.au' + href)
                        img_url = get_player_url_date(full_url)[0]
                        age = get_player_url_date(full_url)[1]
                        dt.loc[index, ('Img', 'Age')] = [[img_url, age]]
                        print(player + ' age is : ' + str(age) + ' ' + img_url)
                        dt.to_csv('DimPlayer.csv', mode='a', index=False)

    print('Complete')


# !!!!!if want to use different types of data, just change the tags below!!!!
# get each player's data
get_selected_data('DimPlayer')
