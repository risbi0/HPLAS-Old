import pandas as pd
import variables

def main():
    dct = {}
    for name in BRANCH:
        try:
            dct[name] = round(variables.livestream_details[name]['topics'][TOPIC][1] / 3600)
        except KeyError:
            continue

    if BRANCH == variables.HOLOLIVE:
        places = 20
        name = 'hololive'
    else:
        places = 10
        name = 'holostars'

    top_20 = pd.DataFrame.from_dict(dct, orient='index').sort_values(0, ascending=False).head(places)
    top_20.sort_values(0).to_csv(f'output/{name}_{TOPIC}.csv', sep='\t', header=None)

if __name__ == '__main__':
    BRANCH = variables.HOLOLIVE
    TOPIC = 'singing'
    main()