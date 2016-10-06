# RCP_averages
Python script for getting a spreadsheet of RealClearPolitics poll averages by date.

RealClearPolitics has a widely-used poll average for each state in a presidential election year, as well as a national poll average.
Some people out there may find such data useful, so I'm making this script public.

RCP has a system for getting these polling averages by day and by state in JSON; each poll average page (eg 2016 Presidential Election in Ohio 4-way)
has a number, which can be found in the URL for that page (eg the previous example is at the URL http://www.realclearpolitics.com/epolls/2016/president/oh/ohio_trump_vs_clinton_vs_johnson_vs_stein-5970.html with the number 5970).

The state_nums.csv included here is a csv that maps those URLs to their state and their number for 2-way presidential
polls in battleground states in 2016. Change this spreadsheet for whichever polling averages you want to scrape.

Run the script by running the following in your terminal:
python rcp_avg_scraper.py

Change the time period for which you want data by altering the variables at the top of the script, in accordance with the instructions in the comments.
The default is to get all data for all time available.

Credit to Nick Topousis for the helpful code that parses the json in lines 32-42.
