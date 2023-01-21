const fs = require('fs');
const HolodexApiClient = require('holodex.js').HolodexApiClient;
const videoIds = require('../json/channel_vid_ids.json');
const videoDetails = require('../json/livestream_details.json');

const start = performance.now();
const client = new HolodexApiClient({
    apiKey: process.env.API_KEY
});

const NAMES = [
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
    'miyabi', 'kira', 'izuru', 'aruran', 'rikka',
    'astel', 'temma', 'roberu',
    'kaoru', 'shien', 'oga',
    'fuma', 'uyu', 'gamma', 'rio',
    'altare', 'magni', 'axel', 'vesper',
    'bettel', 'flayon', 'hakka', 'shinri'
];
const excludedTopics = ['original_song', 'music_cover', 'shorts', 'animation'];

(async () => {
    for (let i = 0; i < NAMES.length; i++) {
        const NAME = NAMES[i];
        const targetIds = videoIds[NAME];
        const topicIds = {};
        const details = [];
        let counter = 0, unavailableVideos = 0, unavailableVideosLength = 0;
        
        await new Promise((resolve) => {
            (async () => {
                for (let index = 0; index < targetIds.length; index++) {
                    client.getVideo(targetIds[index]).then((video) => {
                        if (!excludedTopics.includes(String(video.topic).toLocaleLowerCase()) &&
                            // aribtrary duration to exclude most untagged/non-stream videos
                            video.videoType === 'stream' && video.duration > 360) {
                            // details
                            details.push({
                                'id': targetIds[index],
                                'title': video.title,
                                'duration': video.duration,
                                'date': video.availableAt.toISOString()
                            });
                            // topics
                            if (!(video.topic in topicIds)) {
                                topicIds[video.topic] = [];
                                topicIds[video.topic][0] = 0;
                                topicIds[video.topic][1] = 0;
                            }
                            topicIds[video.topic][0] += 1;
                            topicIds[video.topic][1] += video.duration;
                            // missing
                            if (video.status === 'missing') {
                                unavailableVideos += 1;
                                unavailableVideosLength += video.duration;
                            }
                        }
                        counter += 1;
                        console.log(`${counter}/${targetIds.length}: ${video.title}`);
                        if (counter === targetIds.length) resolve();
                    })
                    await new Promise((resolve) => setTimeout(resolve, 333));
                }
            })()
        }).then(() => {
            videoDetails[NAME] = {};
            videoDetails[NAME]['missing'] = unavailableVideos;
            videoDetails[NAME]['missing_length'] = unavailableVideosLength;
            videoDetails[NAME]['topics'] = topicIds;
            videoDetails[NAME]['details'] = details;
        
            const newFile = JSON.stringify(videoDetails);
            fs.writeFile('json/livestream_details.json', newFile, () => {
                console.log('JSON data is saved.');
                console.log(`Topics length: ${Object.keys(videoDetails[NAME]['topics']).length}`);
                console.log(`Details length: ${videoDetails[NAME]['details'].length}`);
                console.log(`Time elapsed (HH:MM:SS): ${new Date(performance.now() - start).toISOString().substr(11, 8)}`);
            });
        })
    }
})()