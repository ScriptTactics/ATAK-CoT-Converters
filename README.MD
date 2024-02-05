# ATAK-CoT-Converters

This repository is aimed at hosting all my CoT converter scripts for any data I add to ATAK.


## Traffic Cameras

After watching this [video](https://www.youtube.com/watch?v=5ZQQywmsOvY) I scoured the internet for a large data set of video cameras.

I eventually landed upon [Maryland's GIS](https://data.imap.maryland.gov/) data site which contained publicly viewable traffic cameras.

**If you find other state government websites that contain public traffic cam data create an issue on this repo so I can add it to the parser.**


### createDataPackage.py

Run `python createDataPackage.py` in the root directory of the state you want Traffic Cams for and the application will print out folders organized by region, county, towns, or any other grouping specified in the kml.

Each folder contains its own grouping of sensors, and video streams linked to each sensor. Then there is a manifest with a `MANIFEST` folder for each folder.

Zip up the contents inside each of the region folders and copy those over to your ATAK device. Then you should be able to see the traffic cams.

Ex: Annapolis -> select all -> right click -> compress -> save to annapolis_traffic_cams.zip.
Copy that zip over to your ATAK EUD and import.

Example below:
![Cam](/images/cams.png)
![Icon](/images/showFeed.jpeg)
![Feed](/images/feed.png)