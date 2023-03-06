# HPLAS-Old

**NOTE**: This is the old version that uses Excel for data visualization. The updated version uses Streamlit and Plotly which is published [here](https://github.com/risbi0/Hololive-Production-Livestream-Activity-Statistics).

Data was gathered using [Holodex API](https://holodex.stoplight.io/) with the [holodex.js](https://github.com/HolodexNet/holodex.js) library. Python for data manipulation. MS Excel for visualization with VBA to automate the generation of heatmaps and most of the charts.

This can also work for any other Vtuber that have been has a channel page in Holodex.

### Setup

Install libraries with `pip install -r requirements.txt` and `npm install`.

### Scripts

`holodexVidIds.js` extracts all video ID's of a specific VTuber in its Holodex channel page. It is entered in the dev console where it loops with a delay to let all the links to render on each page, and extract them using the DOM API. The printed result is put in `channel_vid_ids.json`.

`holodexApiClient.js` queries the Holodex API through an array of ID's in `channel_vid_ids.json`, and extracts the interested details in the response. Data is stored in an object and then saved into a JSON file named `livestream_details.json`.

`process_data.py` iterates through the data in `livestream_details.json` and processes it to generate statistics for the heatmap, stream duration count, and other stats.

`macro.vba` automates the creation of most of the data visualizations for each holopro talent. It is already included in the Excel file. It is responsible for copy pasting data to the heatmap, applying conditional formatting for the heatmap, talent-specific colors, and other stats.

The macro does most of the work and the only manual task left (aside from compiling them for a post) is reimporting the CSV files in the `staging` sheet (on the off chance of an update).

### Excel Sheets Overview

`main` is where most of the statistics is stored, such as total and average stream time, and shortest and longest streams. It is referenced by the macro to apply it to each of the talents' sheets.

`group-tables` compares statistics generation-wide and also agency-wide.

`colors` stores all the talent-specific colors primarily used for the heatmap (it's also shown in `COLORS.md`). It is referenced by the macro to apply it to each of the talents' sheets.

`staging` is where all the data for the heatmap, stream duration count, stream count for each day, and topics, are stored. Data is imported using the "From Text/CSV", action which isn't in the ribbon by default, you have to search it in the search bar. Data are spaced constantly since the macro copies it to paste it to its respective talent sheet. They should be arranged according to the names in the `main` sheet so the right data goes to the right person.

`template` is the framework worksheet for the heatmap and other stats of the talents. It is duplicated by the macro which applies all the needed data and styling.

#### Websites Used

[Hololive's Virtual YouTuber Wiki page](https://virtualyoutuber.fandom.com/wiki/Hololive) for getting the main colors for each of the holopro memebers (color picker on their backgrounds), though I changed a few that's too bright, or just what I think better suits them.

[color-hex](https://www.color-hex.com) for getting the lighter tints and complementary colors.

#### Notes

The Holodex API doesn't categorize the videos if they're livestreams or not, nor have a separate section of them in their website. Fortunately their API applies topics to the videos, so I can exclude songs and shorts. I also set a minimum duration of more than 360 seconds for a video to be considered a stream, which takes care most of the topic-less videos.

There's an old version of the heatmaps and charts that only count current archived streams, since I initially used YouTube Data API to get the video details. Until I discovered Holodex's API and found that it stores the same data I was looking for, and even more with topics and details about unarchived videos, which made it possible to make visualisations about Rushia (and also former Holostars member, Kaoru).
