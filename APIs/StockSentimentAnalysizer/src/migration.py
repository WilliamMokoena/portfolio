import os
import datetime as dt
import json
from collections import Counter


def Migrate(timespan):
    '''
    Reads all the data cached, combines it and returns the result

    params:
        timespan: str // 'hour', 'day', 'week'

    returns:
        stores: dict
    '''
    cwd = os.getcwd()
    cache_dir = f'{cwd}/data'
    stores = [
        file for file in os.listdir(cache_dir)
        if f'{timespan}.json' in file]

    combined_store = {}
    for store in stores:
        name_sp = store.split('_')
        src = name_sp[0]

        with open(f'{cache_dir}/{store}') as file:
            contents = json.load(file)

        if src in combined_store.keys():
            combined_store[src] = contents

        else:
            combined_store[src] = contents

    return combined_store


def is_fresh(timespan):
    files = os.listdir('./cache')
    date_time = dt.datetime.now()

    h = date_time.hour
    d = date_time.day
    if timespan == 'hour':
        fresh_file = f'{d}d_{h}h.json'
        if fresh_file in files:
            return fresh_file
        else:
            return 0

    if timespan == 'day':
        fresh_file = f'{d}d.json'
        if fresh_file in files:
            return fresh_file
        else:
            return 0

    else:
        return None


def Aggregate(list_len, timespan):
    '''
    Combines cache data to make a list of the top and returns the result

    params:
        list_len: int
        timespan: str // 'hour', 'day', 'week'

    returns:
        stores: dict
    '''

    # Load from cache
    any_freshfile = is_fresh(timespan)
    if any_freshfile != 0 and any_freshfile != None:
        with open(f'./cache/{any_freshfile}', 'r') as f:
            data = json.load(f)

        return [{'Origin': '1'}, {'data': data}]

    elif any_freshfile == None:
        return {'Error': 'No data found for the timespan given'}

    # Pull from API data
    else:

        data = Migrate(timespan)
        sources = data.keys()
        # Create a new dict containing only the values of the src of the data
        stock_only_data = []
        for src in sources:
            stock_only_data.append(data[src])

        # Combine the data into a single dict
        stock_data_keys = []
        for stock_data in stock_only_data:
            stock_data_keys.append(stock_data.keys())

        # Search for each key in each stock_only_data dict
        assemble_stock_data = {}
        for keys in stock_data_keys:
            for key in keys:
                for stock_data in stock_only_data:
                    try:

                        if key not in assemble_stock_data.keys():
                            if key in stock_data.keys():
                                assemble_stock_data[key] = {
                                    'freq': [stock_data[key]['freq']],
                                    'sentiment_score': [stock_data[key]['sentiment_score']]
                                }
                        elif key in stock_data.keys():
                            assemble_stock_data[key]['freq'].append(
                                stock_data[key]['freq'])
                            assemble_stock_data[key]['sentiment_score'].append(
                                stock_data[key]['sentiment_score'])

                    except ValueError:
                        continue

        # Compress the freq and sentiment_score values
        for stock in assemble_stock_data.keys():
            sum_freqs = sum(assemble_stock_data[stock]['freq'])

            sum_sent_scores = sum(
                assemble_stock_data[stock]['sentiment_score'])
            len_sent_scores = len(
                assemble_stock_data[stock]['sentiment_score'])
            avg_sent_score = sum_sent_scores/len_sent_scores

            assemble_stock_data[stock]['freq'] = sum_freqs
            assemble_stock_data[stock]['sentiment_score'] = round(
                avg_sent_score, 5)

        # Sort all the data by freq
        sorted_freqs_ls = []
        stock_freq_ls = []
        for stock in assemble_stock_data.keys():
            stock_freq = assemble_stock_data[stock]['freq']
            stock_freq_ls.append((stock, stock_freq))
            sorted_freqs_ls.append(stock_freq)
            sorted_freqs_ls = sorted(sorted_freqs_ls)

        sorted_freqs_ls = [i for n, i in enumerate(sorted_freqs_ls)
                           if i not in sorted_freqs_ls[:n]]

        sorted_freqs_ls = sorted(sorted_freqs_ls, reverse=True)
        sorted_stock_ls = []
        for freq in sorted_freqs_ls:
            for fs in stock_freq_ls:
                k = fs[0]
                v = fs[1]
                if v == freq:
                    sorted_stock_ls.append({
                        k: {
                            'freq': assemble_stock_data[k]['freq'],
                            'sentiment_score': assemble_stock_data[k]['sentiment_score']
                        }
                    })

        date_time = dt.datetime.now()

        if timespan == 'hour':
            cache_file = f'./cache/{date_time.day}d_{date_time.hour}{timespan[0]}.json'

        if timespan == 'day':
            cache_file = f'./cache/{date_time.day}{timespan[0]}.json'

        with open(f'{cache_file}', 'w') as f:
            json.dump(sorted_stock_ls, f)

        return [{'Origin': '0'}, {'data': sorted_stock_ls[0:list_len]}]
