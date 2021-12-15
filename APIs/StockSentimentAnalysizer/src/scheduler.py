import os
import time
import json
import datetime as dt
from Stock_Sentiment_Analysis import main as stock_sent_analysis


def run_stock_analysis(timespan, subreddit):
    print(f'[INFO] Pulling {timespan} data for {subreddit}')
    stock_sent_analysis(timespan, subreddit)


def start():
    '''
    Responsible for scheduling running of the script to pull data from the API
    every 45 minutes for the hourly data and every 6 hours for the day data
    '''

    cwd = os.getcwd()
    data_files = os.listdir(f'{cwd}/data')

    # Getting the socials to query about
    with open('./resources/SOCIALS.json') as f:
        socials = json.load(f)

    while True:
        date_time = dt.datetime.now()
        hour = date_time.hour
        mins = date_time.minute
        secs = date_time.second
        # If for some reason the data folder is empty
        if len(data_files) == 0:
            print(f'[INFO] Restoring data stores')
            subreddits = socials['subreddits']

            for subr in subreddits:
                run_stock_analysis('day', subr)
                run_stock_analysis('hour', subr)

        # If it is 45 mins since the last pull
        elif mins >= 45:
            print('[INFO] Refreshing hourly data')
            subreddits = socials['subreddits']

            for subr in subreddits:
                run_stock_analysis('hour', subr)

            date_time = dt.datetime.now()
            mins = date_time.minute
            secs = date_time.second

            sleep_time = (45*60)+(mins*60+secs)
            print(f'[INFO] Sleeping for {sleep_time} seconds')
            time.sleep(sleep_time)

        # If it is 6 hours since the last pull
        elif hour == 0 or hour == 6 or hour == 12 or hour == 18:
            subreddits = socials['subreddits']

            for subr in subreddits:
                run_stock_analysis('day', subr)

        else:
            sleep_time = 45*60 - (mins*60+secs)
            if sleep_time > 0:
                print(f'[INFO] Sleeping for {sleep_time} seconds')
                time.sleep(sleep_time)


start()
