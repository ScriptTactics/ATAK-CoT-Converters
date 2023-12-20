# ATAK-CoT-Converters

This repository is aimed at hosting all my CoT converter scripts for any data I add to ATAK.

After watching this [video](https://www.youtube.com/watch?v=5ZQQywmsOvY) I scoured the internet for a large data set of video cameras. 

I eventually landed upon [Maryland's GIS](https://data.imap.maryland.gov/) data site which contained publicly viewable traffic cameras.

**If you find other state government websites that contain public traffic cam data create an issue on this repo so I can add it to the parser.**

## The Script

Run `python createDataPackage.py` in the root directory of the project and the application will print out a few different folders.

 - Annapolis
 - Baltimore
 - Eastern Shore
 - Southern MD
 - ungrouped
 - Wash. DC
 - Western MD

I was able to group these together by comparing the `lat/lon` values from the .kml to the [Camera Feeds JSON](https://chart.maryland.gov/DataFeeds/GetCamerasJson). 

Each folder contains its own grouping of sensors, and video streams linked to each sensor. Then there is a manifest with a `MANIFEST` folder for each folder.

Zip up the contents inside each of the folders and copy those over to your ATAK device. Then you should be able to see the traffic cams.