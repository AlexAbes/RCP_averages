# Written by Alex Abrahams October 2016
# With big help from Nick Topousis's original code on parsing the json response

import csv
import json
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, time, timedelta

# WARNING: CURRENT DEFAULT IS TO GET AVERAGE FOR ALL DATES AVAILABLE
# if you have a date range to use, change the date_range variable to True
date_range = False
# and give your start and end dates in the two below variables as (year, month, day)
date_start = date(2016, 10, 3)
date_end = date(2016, 10, 5)

# change the election day as needed: this default is 2016 election day
election_day = date(2016, 11, 8)
list_of_rows = []
header_row = ['Date','Days_until_election','Democrat','Republican','Winning','Margin','State']
# if you don't want/need a header row, then comment out the below line
list_of_rows.append(header_row)

def get_RCP_avg_csv(state_num, state):
    # create the current url for this state
    current_url = 'http://www.realclearpolitics.com/epolls/json/' + str(state_num) + '_historical.js?no_cache='
    # get the response for this url: returns Response 200 if working
    response = requests.get(current_url)
    # get the content from this response
    html = response.content
    # parse this content using BeautifulSoup's html parser
    soup = BeautifulSoup(html, "html.parser")
    # turn the above BeautifulSoup class into unicode
    souptext = soup.encode('ascii', 'ignore').decode('ascii')
    # finds the index in this string where the first ( appears
    a = souptext.find("(")
    # now we get the entire json from the (a+1)th character in to the third-last character
    json_string = souptext[a+1:-3]
    # turn that string into actual json
    parsed_json = json.loads(json_string)
    # we only want the rcp_avg stuff inside the poll key
    poll_list = parsed_json['poll']['rcp_avg']
    # iterate through the objects in the list, which are themselves lists
    for sublist in poll_list:
        # RCP's date is a string, needs to be converted to a datetime object and then converted to a date that can be compared
        sublist['date'] = sublist['date'][:-6]
        date_object = datetime.strptime(sublist['date'], '%a, %d %b %Y %H:%M:%S')
        year = int(date_object.strftime("%Y"))
        month = int(date_object.strftime("%m"))
        day = int(date_object.strftime("%d"))
        date_thing = date(year, month, day)
        # check if user wanted a date range
        if date_range:
            # check if date is in the range specified
            if (date_thing >= date_start) and (date_thing <= date_end):
                # then the date does fall in our range, so we want to add it to our csv
                list_of_cells = []
                list_of_cells.append(date_object.strftime("%m/%d/%Y"))
                # work out the number of days until the election
                diff = election_day - date_thing
                days_until_eday = int(str(diff).rsplit('days,', 1)[0])
                list_of_cells.append(days_until_eday)
                # get the Democrat and Republican numbers: this approach does NOT assume the polls are only 2-way, could be more candidates
                for item in sublist['candidate']:
                    # find the democrat
                    if (item['affiliation'] == 'Democrat'):
                        democrat_num = float(item['value'])
                        list_of_cells.append(democrat_num)
                    # find the republican
                    elif (item['affiliation'] == 'Republican'):
                        republican_num = float(item['value'])
                        list_of_cells.append(republican_num)
                # margin is the margin in favor of the Democrat: i.e. it is positive if D is winning, negative if losing
                margin = democrat_num - republican_num
                # decide who is winning
                if (margin > 0):
                    list_of_cells.append("Democrat")
                elif (margin < 0):
                    list_of_cells.append("Republican")
                else:
                    list_of_cells.append("Tied")
                list_of_cells.append(abs(margin))
                list_of_cells.append(state)
                list_of_rows.append(list_of_cells)
        else:
            list_of_cells = []
            list_of_cells.append(date_object.strftime("%m/%d/%Y"))
            # work out the number of days until the election
            diff = election_day - date_thing
            days_until_eday = int(str(diff).rsplit('days,', 1)[0])
            list_of_cells.append(days_until_eday)
            # get the Democrat and Republican numbers: this approach does NOT assume the polls are only 2-way, could be more candidates
            for item in sublist['candidate']:
                # find the democrat
                if (item['affiliation'] == 'Democrat'):
                    democrat_num = float(item['value'])
                    list_of_cells.append(democrat_num)
                # find the republican
                elif (item['affiliation'] == 'Republican'):
                    republican_num = float(item['value'])
                    list_of_cells.append(republican_num)
            # margin is the margin in favor of the Democrat: i.e. it is positive if D is winning, negative if losing
            margin = democrat_num - republican_num
            # decide who is winning
            if (margin > 0):
                list_of_cells.append("Democrat")
            elif (margin < 0):
                list_of_cells.append("Republican")
            else:
                list_of_cells.append("Tied")
            list_of_cells.append(abs(margin))
            list_of_cells.append(state)
            list_of_rows.append(list_of_cells)


# you could use the above function by itself, outside of the States csv iteration below. For example:
# get_RCP_avg_csv('5633', 'PA')

# open the States csv as a list
with open('state_nums.csv', 'rb') as states_object:
    reader = csv.reader(states_object)
    states_list = list(reader)
    # iterate through the states in this csv, getting the avg for each state
    for row in states_list:
        get_RCP_avg_csv(row[2], row[1])
    # now create the output csv
    outfile = open("./RCP_averages.csv", "wb")
    writer = csv.writer(outfile)
    writer.writerows(list_of_rows)