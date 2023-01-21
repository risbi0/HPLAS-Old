import os, json

curr_file_path = os.path.dirname(__file__)
with open(os.path.join(os.path.dirname(__file__), '../json/livestream_details.json'), encoding='utf8') as file:
    livestream_details = json.load(file)

HOLOLIVE = [
    'hololive',
    'sora', 'roboco', 'miko', 'suisei', 'azki',
    'mel', 'fubuki', 'matsuri', 'haachama', 'aki',
    'aqua', 'shion', 'ayame', 'choco', 'subaru',
    'mio', 'okayu', 'korone',
    'pekora', 'rushia', 'flare', 'noel', 'marine',
    'kanata', 'coco', 'watame', 'towa', 'luna',
    'lamy', 'nene', 'botan', 'polka', 
    'laplus', 'lui', 'koyori', 'chloe', 'iroha',
    'risu', 'moona', 'iofi',
    'ollie', 'anya', 'reine',
    'zeta', 'kaela', 'kobo',
    'calli', 'kiara', 'ina', 'gura', 'ame',
    'irys', 'fauna', 'sana', 'kronii', 'mumei', 'bae',
]

HOLOSTARS = [
    'miyabi', 'kira', 'izuru', 'aruran', 'rikka',
    'astel', 'temma', 'roberu',
    'kaoru', 'shien', 'oga',
    'fuma', 'uyu', 'gamma', 'rio',
    'altare', 'magni', 'axel', 'vesper',
    'bettel', 'flayon', 'hakka', 'shinri'
]

HOLOPRO = HOLOLIVE + HOLOSTARS