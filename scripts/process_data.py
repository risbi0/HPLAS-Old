from variables import HOLOPRO, curr_file_path, livestream_details
from datetime import datetime, timedelta
from pytz import timezone
from time import perf_counter
import pandas as pd
import numpy as np
import os, glob, json, calendar

def timings(time):
    weekday = time.weekday() + 1

    # sunday
    if weekday == 7:
        weekday = 0

    # for list usage
    return time.hour * 60 + time.minute - 1, weekday

def m_to_dhhmm(seconds, showDays):
    days = seconds // 86400
    seconds = seconds % 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60

    if showDays:
        return f'{days}:{hours:02d}:{minutes:02d}'

    return f'{hours}:{minutes:02d}'

def output(var, name):
    folder_name = name.split('_')[0]

    # in dataframe
    df = pd.DataFrame({'0': var})

    # folder if folder doesn't exist
    if not os.path.isdir(f"output/{folder_name}"):
        os.mkdir(f'output/{folder_name}')

    # each value a column, and save as csv
    pd.DataFrame(df['0'].values.tolist()).to_csv(
        os.path.join(os.path.dirname(__file__), f'../output/{folder_name}/{name}.csv'),
        header=False,
        index=False,
        sep='\t'
    )

def to_HHMM(i):
    return f'{str(i.item() // 60).zfill(2)}:{str(i.item() % 60).zfill(2)}'

def consecutive(data):
    # return string of consecutive time ranges in HH:MM format
    arrs = np.split(data, np.where(np.diff(data) != 1)[0] + 1)
    out = ''

    for arr in arrs:
        start_time = to_HHMM(arr[0])

        if arr[0] != arr[-1]:
            end_time = to_HHMM(arr[-1])
            out += f'{(start_time)}-{end_time} '
        else:
            out += f'{start_time} '
    
    return out.strip().replace(' ', ', ')

def main():
    print(f'========================={NAME.upper()}=========================')
    # initialize variables
    heatmap_data = [[0 for _ in range(1440)] for _ in range(7)]
    weekday_data = [0 for _ in range(7)]
    hour_data = [0 for _ in range(12)]
    total_mins = 0
    max_f = []
    max = {
        'title': None,
        'id': None,
        'date': None,
        'length': 0
    }

    # iterate ID's of specified channel
    for detail in livestream_details[NAME]['details']:
        id = detail['id']
        title = detail['title']
        stream_date = detail['date']
        vid_dur = detail['duration']

        print(f"Processing: {title}")

        start_iso = datetime.strptime(stream_date, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Tokyo'))
        end_iso = start_iso + timedelta(seconds=vid_dur)
        # start time & end time in mins since midnigth in JP timezone
        # and day of the week (sun = 0, ..., sat = 6)
        start_time, start_day = timings(start_iso)
        end_time, end_day = timings(end_iso)
        
        # data
        # streams per day
        weekday_data[start_day] += 1

        # stream duration count (mins)
        same_day_stream = start_time <= end_time # check if stream ended on the same day
        duration = end_time - start_time if same_day_stream else 1440 - start_time + end_time
        if duration < 1: duration = 1
        if duration > 720: duration = 720
        hour_data[(duration - 1) // 60] += 1
        
        # stats
        total_mins += round(vid_dur / 60)
        # get longest video
        if duration >= max['length']: 
            # multiple details if theyre of equal duration
            if duration != max['length']:
                max_f.clear()
            
            # details to dictionary
            max['title'] = title
            max['id'] = f'https://youtu.be/{id}'
            max['date'] = start_iso.strftime('%B %d %Y').lstrip('0')
            max['length'] = duration

            # dictionary to list
            max_f.append(max.copy())
        
        # heatmap
        for i in range(1440):
            if (i >= start_time and i <= end_time and same_day_stream) or \
               (i >= start_time and not same_day_stream):
                heatmap_data[start_day][i] += 1
            elif i <= end_time and not same_day_stream:
                heatmap_data[end_day][i] += 1

    # delete old files
    old_files = glob.glob(os.path.join(curr_file_path, f'..\output\{NAME}\*'))
    for file in old_files:
        os.remove(file)

    output(heatmap_data, NAME)
    output(weekday_data, f'{NAME}_wd')
    output(hour_data, f'{NAME}_hr')

    # top 10 topics by streaming hrs
    topics_df = pd.DataFrame.from_dict(livestream_details[NAME]['topics'], orient='index')
    top_10_topics = topics_df.sort_values(1, ascending=False).drop('undefined').head(10)
    top_10_topics[1] = top_10_topics[1].apply(lambda x: round(x / 3600))
    top_10_topics.sort_values(1).to_csv(
        os.path.join(os.path.dirname(__file__), f'../output/{NAME}/{NAME}_tp.csv'),
        header=False,
        sep='\t'
    )

    # save stats to main csv
    livestream_count = len(livestream_details[NAME]['details'])
    avg_mins = round(total_mins / livestream_count)

    df = pd.read_csv('output/data.csv', delimiter='\t', index_col=[0]) # add new rows in other file
    df.loc[NAME, 'count'] = livestream_count
    df.loc[NAME, 'total_hrs'] = round(total_mins / 60)
    df.loc[NAME, 'total_f'] = m_to_dhhmm(total_mins * 60, True)
    df.loc[NAME, 'avg_mins'] = avg_mins
    df.loc[NAME, 'avg_f'] = m_to_dhhmm(avg_mins * 60, False)
    df.loc[NAME, 'missing'] = livestream_details[NAME]['missing']
    df.loc[NAME, 'missing_hr'] = round(livestream_details[NAME]['missing_length'] / 3600, 2)

    titles = ', '.join(dct['title'] for dct in max_f)
    id = ', '.join(dct['id'] for dct in max_f)
    dates = ', '.join(dct['date'] for dct in max_f)
    df.loc[NAME, 'long_title'] = titles
    df.loc[NAME, 'long_id'] = id
    df.loc[NAME, 'long_date'] = dates
    df.loc[NAME, 'long_length'] = max_f[0]['length']

    weekdays = list(calendar.day_name)
    # shift sunday to first position
    weekdays = weekdays[-1:] + weekdays[:-1]

    # overlap stats
    holo_df = pd.read_csv(
        os.path.join(curr_file_path, f'../output/{NAME}/{NAME}.csv'),
        delimiter='\t',
        header=None
    )
    df_arr = holo_df.to_numpy()
    max_overlap = df_arr.max()
    max_str = ''

    for index, row in holo_df.iterrows():
        row_arr = row.to_numpy()
        max = np.where(row_arr == max_overlap)[0]
        
        if max.size != 0:
            max_str += f'{weekdays[index]} ({consecutive(max)}) '
    
    df.loc[NAME, 'most_overlap'] = f'{max_str}{max_overlap}'

    df.to_csv(os.path.join(curr_file_path, '../output/data.csv'), sep='\t')

if __name__ == '__main__':
    start = perf_counter()
   
    for holomem in HOLOPRO:
        NAME = holomem
        main()

    print(f'Done. Time took: {round(perf_counter() - start, 2)} seconds.')