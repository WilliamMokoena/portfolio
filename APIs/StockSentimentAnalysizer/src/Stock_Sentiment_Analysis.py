import sys
import os
import time
import json
import re
from collections import Counter
import praw
# import tweepy
import nltk
from yahooquery import Ticker
from pytickersymbols import PyTickerSymbols


class Sentiment_Analysis:
    '''
    Uses classifier to determine a text's sentiment
    '''

    def __init__(self):
        try:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            self.sentiment_analyzer = SentimentIntensityAnalyzer()

        except LookupError:
            nltk.download('vader_lexicon')
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
            self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def determine_sentiment(self, text):
        '''
        Uses the VADER classifier to determine the sentiment of a give phrase or
        sentence

        params:
            text: str // A sentence or phrase
        '''
        pscores = self.sentiment_analyzer.polarity_scores(text)
        return pscores


class Reddit_API_Interface:
    '''
    Custom Reddit API interface class
    '''

    def __init__(self, ID, SECRET, USERNAME):
        '''
        Constructor needs to configure the Reddit API

        params:
            ID: str,
            SECRET: str,
            USERNAME: str
        '''
        self.reddit = praw.Reddit(
            client_id=ID,
            client_secret=SECRET,
            user_agent=f"script:sentiment-analysis:v0.0.1 (by {USERNAME})"
        )

    def get_top_submissions(self, subreddit, timespan, max_comments):
        '''
        Fetches all the top submissions within the give timespan

        params:
            subreddit: str // Name of the subreddit
            timespan: str // e.g 'hour', 'day' and 'week'
            max_comments: int // The max number of comments to fetch per submission

        return:
            posts: list<dict> // List of submissions
            /* {
                    title: str,
                    text: str,
                    comments: list
                }
            */
        '''
        log = f'[INFO] Getting top reddit submissions'
        print(log)
        subr = self.reddit.subreddit(subreddit)
        submissions = subr.top(timespan)

        posts = []
        for sub in submissions:
            post = {
                'title': sub.title,
                'text': sub.selftext,
                # 'num_comments': sub.num_comments,
                # 'up_votes': sub.ups,
                # 'down_votes': sub.downs,
                # 'url': sub.url,
                # 'time_created': sub.created
            }

            sub.comments.replace_more(limit=max_comments)
            comment_list = sub.comments.list()

            comments = []
            for comment in comment_list:
                comments.append(comment.body)

            post['comments'] = comments

            posts.append(post)

        return posts


def write_file(filename, filetype, obj):
    '''
    Writes an object to a specified file

    params:
        filename: str
        filetype: str
        obj: object
    '''
    if filetype == 'json':
        with open(f'{filename}.json', 'w') as f:
            json.dump(obj, f)

    else:
        return 'Filetype Unsupported'


def model_data(submissions):
    '''
    params:
        submissions: { reddit.submissions, submission.comments }

    returns:
        reddit_data: dict
        /* {
            position: {
                title:str,
                text:str,
                comments: list
                }
            }
        */
    '''
    log = f'[INFO] Modelling data'
    print(log)
    id_num = 0
    reddit_data = {}

    # Modeling passed data
    for id_num in range(0, len(submissions)):
        submission = submissions[id_num]
        reddit_data[str(id_num)] = submission
        id_num += 1

    return reddit_data


def identify_tickers(text):
    '''
    Uses common regex pattern of tickers to find what seems to be possible
    tickers from the given text and their frequency.

    params:
        text: str

    returns:
        tickers: dict
        /*
        e.g {'TSLA': 5}
        */
    '''
    # Find what seems to a ticker
    pattern = "[$]?\\b[A-Z]{1,5}\\b"
    pos_tickers = re.findall(pattern, text)
    if len(pos_tickers) > 0:
        pot_tickers = [txt for txt in pos_tickers if txt.isupper()]

        if len(pos_tickers) > 0:
            cap_tickers = [ticker.upper()
                           for ticker in pot_tickers if is_ticker(ticker)]

            # Count the frequency of each ticker
            ticker_count = Counter(cap_tickers)
            tickers = dict(ticker_count)

            return tickers

        else:
            return {}

    else:
        return {}


def is_ticker(ticker_candidate):
    '''
    Searches for the given 'ticker_candidate' in the registry. If its not there it
    will try to update the registry and if it is still not present it will try
    yahoo finance API.

    params:
        ticker_candidate: str

    returns:
        verdict: boolean
    '''
    def check_registry(ticker):
        '''
        Looks up the given ticker in the registry
        '''
        with open('./resources/STOCK_TICKERS.json', 'r') as f:
            known_tickers = json.load(f)

        return known_tickers[ticker]

    def update_registry():
        '''
        Checks to see if the registry is up-to-date. If it isn't the it will be
        updated.
        '''
        mtime = os.path.getmtime('./resources/STOCK_TICKERS.json')
        time_lapse = time.time() - mtime

        # If the last time the registry was updated is less than 30 days then no
        # update is needed
        if time_lapse < 2_000_000:
            return

        else:
            stock_data = PyTickerSymbols()
            _data = stock_data.get_all_stocks()
            ticker_data = {}

            for stock in _data:
                ticker = stock['symbol']
                name = stock['name']
                ticker_data[ticker] = name

            with open('./resources/STOCK_TICKERS.json', 'w') as f:
                json.dump(ticker_data, f)

    # [NOTE] [WARNING] [HACK] : This is a hack to handle 'I' and 'A'
    if ticker_candidate == 'I' or ticker_candidate == 'A':
        return False

    try:
        company_name = check_registry(ticker_candidate)
        if company_name:
            verdict = True

    except KeyError:
        update_registry()

        try:
            company_name = check_registry(ticker_candidate)
            if company_name:
                verdict = True
        except KeyError:
            verdict = False
            pass
            # [NOTE] [OPTIMISATION] : this query (following code) slows down the
            # script since it's called every time this exception is hit.

            # stock = Ticker(ticker_candidate)
            # price_info = stock.price

            # if type(price_info[ticker_candidate]) == type(''):
            #     verdict = False

            # elif type(price_info) == type({}):
            #     verdict = True

    return verdict


def get_sentimentality(modeled_submissions):
    '''
    Calls 'Sentiment_Analysis.determine_sentiment()' for every given piece of text
    and user results to determine average setimentality of a post.

    params:
        modeled_submissions: dict // result of model_data()

    returns:
        data_sentimentality: dict
    '''
    log = f'[INFO] Determining sentiments polarity_scores of reddit submissions'
    print(log)
    sentiment_analysis = Sentiment_Analysis()
    determine_sentiment = sentiment_analysis.determine_sentiment

    data_sentimentality = {}
    for pos in range(0, len(modeled_submissions)):
        position = str(pos)
        title = modeled_submissions[position]['title']
        body = modeled_submissions[position]['text']
        comments = modeled_submissions[position]['comments']

        title_sentiment = determine_sentiment(title)
        body_sentiment = determine_sentiment(body)

        comments_sentiments = []
        for comment in comments:
            comment_sentiment = determine_sentiment(comment)
            comments_sentiments.append(comment_sentiment)

        data_sentimentality[position] = {
            'title_sentiment': title_sentiment,
            'body_sentiment': body_sentiment,
            'comments_sentiments': comments_sentiments
        }

    return data_sentimentality


def calculate_sentimentality(data):
    '''
    Takes in results from 'get_sentimentality()' calculates the average of all
    comments

    params:
        data: dict // Result from get_sentimentality()

    returns:
        posts_sentiments: dict
        /*
        {
            index: {
                sentimentality: str
            }
        }
        */
    '''
    log = f'[INFO] Determining average sentiments of data'
    print(log)
    posts_sentiments = {}
    for index in range(0, len(data)):
        post = data[str(index)]

        title_sentiment = post['title_sentiment']['compound']
        body_sentiment = post['body_sentiment']['compound']
        comments_sentiments_list = post['comments_sentiments']

        comments_sentiments = []

        for comment_sentiment in comments_sentiments_list:
            comments_sentiments.append(comment_sentiment['compound'])

        if len(comments_sentiments) != 0:
            calc_sent = (sum(comments_sentiments) /
                         len(comments_sentiments))

            comment_sentiment = round(calc_sent, 5)

        else:
            comment_sentiment = 0

        sentiments_list = [title_sentiment, body_sentiment, comment_sentiment]

        overall_sentiment = (sum(sentiments_list)/len(sentiments_list))

        posts_sentiments[str(index)] = {'sentimentality': overall_sentiment}

    return posts_sentiments


def get_discussed_stocks(ticker_data):
    '''
    Extracts the stock tickers and their frequency

    params:
        ticker_data: dict

    returns:
        stocks_discussed: dict
        /*
        {
        'index': {
            'sentiment': ''
            'ticker':
            }
        }
        */
    '''
    stocks_discussed = {}

    for index in range(0, len(ticker_data)):
        post_tickers = ticker_data[str(index)]
        stocks_discussed[str(index)] = {}

        discussed_stocks = stocks_discussed[str(index)]

        if post_tickers != None:
            title_tickers = post_tickers['title_tickers']
            title_tickers_counter = Counter({})
            for index in range(0, len(title_tickers)):
                title_tickers_counter += Counter(title_tickers)

            body_tickers = post_tickers['body_tickers']
            body_tickers_counter = Counter({})
            for index in range(0, len(body_tickers)):
                body_tickers_counter += Counter(body_tickers)

            comments_tickers = post_tickers['comments_tickers']
            comments_tickers_counter = Counter({})
            for index in range(0, len(comments_tickers)):
                d = comments_tickers[index]
                comments_tickers_counter += Counter(d)

            overall_ticker_counter = title_tickers_counter + \
                body_tickers_counter+comments_tickers_counter

            if 'sentimentality' in discussed_stocks.keys():
                discussed_stocks['sentimentality'] = discussed_stocks['sentimentality'] + \
                    post_tickers['sentimentality']

            else:
                discussed_stocks['sentimentality'] = post_tickers['sentimentality']

            for ticker in overall_ticker_counter.keys():
                discussed_stocks[ticker] = overall_ticker_counter[ticker]

    return stocks_discussed


def main(timespan, sub_reddit):
    log = f'[INFO] Running Stock_Sentiment_Analysis main function with params: timespan={timespan} and subreddit={sub_reddit}'
    print(log)
    with open('./resources/SECRETS.json', 'r') as f:
        creds = json.load(f)

    # Parsing the reddit API credentials
    r_creds = creds['reddit']
    r_id = r_creds['ID']
    r_secret = r_creds['SECRET']
    r_username = r_creds['USERNAME']

    # Initialise the API handler
    red_api = Reddit_API_Interface(r_id, r_secret, r_username)

    # Make call for a todays top submissions
    red_submissions = red_api.get_top_submissions(
        subreddit=sub_reddit,
        timespan=timespan,
        max_comments=10
    )

    # Model the data for proper handling by the sentimentality determiners
    reddit_data = model_data(red_submissions)

    # Getting the sentiments of each submission and its comments
    sentimentality_data = get_sentimentality(reddit_data)
    post_sentimentality = calculate_sentimentality(sentimentality_data)

    # Getting tickers mentioned in the text
    ticker_data = {}
    log = f'[INFO] Getting tickers mentioned in the text'
    print(log)
    for sub_index in range(0, len(reddit_data)):
        sentiment = post_sentimentality[str(sub_index)]['sentimentality']

        sub = reddit_data[str(sub_index)]

        title = sub['title']
        sub_body = sub['text']
        comments = sub['comments']

        title_tickers = identify_tickers(title)
        sub_body_tickers = identify_tickers(sub_body)

        comments_tickers = []
        for comment in comments:
            c_tickers = identify_tickers(comment)
            comments_tickers.append(c_tickers)

        if len(title_tickers) > 0 or len(sub_body_tickers) > 0:
            ticker_data[str(sub_index)] = {
                'title_tickers': title_tickers,
                'body_tickers': sub_body_tickers,
                'comments_tickers': comments_tickers,
                'sentimentality': sentiment
            }

        else:
            ticker_data[str(sub_index)] = None

    discussed_stocks_raw = get_discussed_stocks(ticker_data)
    discussed_stocks = get_discussed_stocks(ticker_data)
    extracted_pscores = {}
    for index in range(0, len(discussed_stocks)):
        if 'sentimentality' in discussed_stocks[str(index)].keys():
            extracted_pscores[str(index)] = discussed_stocks[str(
                index)].pop('sentimentality')

    stock_counter = Counter({})
    for index in range(0, len(discussed_stocks)):
        d = discussed_stocks[str(index)]
        stock_counter += Counter(d)

    final_sent_data = {}
    scaled_sent_data = {}
    # Linking the the extracted scores to their tickers and scale them up based on the
    # tickers frequency then store the scaled score in a list and get the average
    log = f'[INFO] Linking tickers to the polarity scores of text in which they were mentioned'
    print(log)
    for index in discussed_stocks_raw.keys():
        for stock in stock_counter.keys():
            if stock in discussed_stocks_raw[index].keys():
                freq = discussed_stocks_raw[index][stock]
                score = extracted_pscores[index]
                scaled_sent = score * freq

                if stock in scaled_sent_data.keys():
                    scaled_sent_data[stock].append(scaled_sent)

                else:
                    scaled_sent_data[stock] = [scaled_sent]

    log = f'[INFO] Assembling final data model'
    print(log)
    for stock in scaled_sent_data.keys():
        sent_data_list = scaled_sent_data[stock]
        final_sent = sum(sent_data_list)/stock_counter[stock]
        final_sent_data[stock] = {
            'freq': stock_counter[stock],
            'sentiment_score': final_sent
        }

    # Caching the data
    _filename = f'./data/{sub_reddit}_{timespan}'
    _filetype = 'json'

    # Write a json to store the collected data
    write_file(filename=_filename, filetype=_filetype, obj=final_sent_data)

    return 0
