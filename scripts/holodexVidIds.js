/*
    Script to extract all YouTube video ID's of a channel in Holodex.
    Go to a VTuber's Holodex channel page and under the Videos tab and enter the run the script in the dev console.
    Returns a key-value pair that is the holomem name and an string array of ID's, to be put in channel_vid_id.json.
*/

// get key name based on channel name
const hololiveNames = [
    'hololive',
    'sora', 'roboco', 'miko', 'suisei', 'azki',
    'mel', 'fubuki', 'matsuri', 'haachama', 'aki',
    'aqua', 'shion', 'ayame', 'choco', 'subaru',
    'mio', 'okayu', 'korone',
    'pekora', 'rushia', 'flare', 'noel', 'marine',
    'kanata', 'coco', 'watame', 'towa', 'luna',
    'nene', 'polka', 'botan', 'lamy',
    'laplus', 'lui', 'koyori', 'chloe', 'iroha',
    'risu', 'moona', 'iofi',
    'ollie', 'anya', 'reine',
    'zeta', 'kaela', 'kobo',
    'calli', 'kiara', 'ina', 'gura', 'ame',
    'irys', 'fauna', 'sana', 'kronii', 'mumei', 'bae',
    'miyabi', 'kira', 'izuru', 'aruran', 'rikka',
    'astel', 'temma', 'roberu',
    'kaoru', 'shien', 'oga',
    'fuma', 'uyu', 'gamma', 'rio',
    'altare', 'magni', 'axel', 'vesper',
    'bettel', 'flayon', 'hakka', 'shinri'
];
const channelName = document.querySelector('div.channel-container div.v-list-item__title a[href]').innerText.split(' ').map((string) => string.toLowerCase());
const keyName = hololiveNames.filter((name) => channelName.includes(name))[0] || '';
const nextPage = document.querySelectorAll('button.v-pagination__navigation')[1];
const paginationButtons = document.querySelector('ul.v-pagination');
const pageAmount = parseInt(paginationButtons.children[paginationButtons.childElementCount - 2].innerText);
let ids = '', counter = 0;

const loop = setInterval(() => {
    // get elements containing the links
    const links = document.querySelectorAll('a.video-card-text');
    // extract id
    links.forEach((link) => ids += `"${link.href.match(/(?<=watch\/).{11}/g)[0]}", `);
    // go to next page
    nextPage.click();
    
    counter += 1;
    if (counter === pageAmount) {
        clearInterval(loop);
        console.log(`"${keyName}": [${ids.slice(0, -2)}],`);

        const idArray = ids.split(',');
        const extractedLength = idArray.length;
        const noDupesLength = [...new Set(idArray)].length;

        console.log(`Length: ${extractedLength}`);

        if (extractedLength !== noDupesLength) {
            console.warn('Dupes found in ID array which most likely means incomlete ID extraction. Try again.');
            console.log(`Length w/o dupes: ${noDupesLength}`);
        }
    }
}, 3000);