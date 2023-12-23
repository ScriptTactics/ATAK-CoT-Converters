# ATAK-CoT-Converters

This repository is aimed at hosting all my CoT converter scripts for any data I add to ATAK.


## Traffic Cameras

After watching this [video](https://www.youtube.com/watch?v=5ZQQywmsOvY) I scoured the internet for a large data set of video cameras.

I eventually landed upon [Maryland's GIS](https://data.imap.maryland.gov/) data site which contained publicly viewable traffic cameras.

**If you find other state government websites that contain public traffic cam data create an issue on this repo so I can add it to the parser.**

### Schema's

If you can get a KML of the cameras you want to add take a look at the schema in the file. You want to match the schema definition to the Maryland schema, as the script was built for that schema. Only a few minor changes should be necessary. The example below describes that process.

MD Schema:
```xml
<Schema name="Maryland_Traffic_Cameras___Traffic_Cameras" id="Maryland_Traffic_Cameras___Traffic_Cameras">
	<SimpleField name="rowid" type="int"></SimpleField>
	<SimpleField name="ID" type="string"></SimpleField>
	<SimpleField name="location" type="string"></SimpleField>
	<SimpleField name="url" type="string"></SimpleField>
	<SimpleField name="CCTVPublicURL" type="string"></SimpleField>
	<SimpleField name="hlsurl" type="string"></SimpleField>
	<SimpleField name="Latitude" type="float"></SimpleField>
	<SimpleField name="Longitude" type="float"></SimpleField>
</Schema>
```

Example

NY
```xml
<Schema name="NYCDOT_TrafficCameras" id="NYCDOT_TrafficCameras">
	<SimpleField name="Name" type="string"></SimpleField>
	<SimpleField name="Description" type="string"></SimpleField>
	<SimpleField name="ID" type="float"></SimpleField>
	<SimpleField name="LAT" type="float"></SimpleField>
	<SimpleField name="LON" type="float"></SimpleField>
	<SimpleField name="ACTIVE" type="string"></SimpleField>
	<SimpleField name="LOCATION" type="string"></SimpleField>
	<SimpleField name="LIVEID" type="float"></SimpleField>
	<SimpleField name="URLIMAGE" type="string"></SimpleField>
	<SimpleField name="URLANIM" type="string"></SimpleField>
</Schema>
```

Open the file in VScode or similar editor, and set the name of the "video link" to hlsurl.


In the `NYCDOT_TrafficCameras.kml` update the value `URLIMAGE` to `hlsurl`. You can do this easily by highlighting the text, pressing `ctrl+f`. Then in the popup that appears on the top right of the screen, press the arrow to expand the popup, in the box that says `Replace` type `hlsurl`. Then press the replace all button next to the `Replace` box.

\* if the text is capital or sorthand you will have to change it as well. I will look into updating the logic to handle that in the future but for now it should only take a few more seconds for you.
- LAT -> Latitude
- LON -> Longitude
- URLIMAGE -> hlsurl



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

### KML

If you wish to just use the KML file that is in the folder, it's suggested that you run the `format.py` script to add a name to each element. If you were to import the KML without running the script all the elements will be imported into ATAK without a name.

The script should require little modification if you followed the steps in the [Schema's](#schemas) section. All you would need to do is change these 2 variables:

1. `kml_file_path`
1. `new_kml_file_path`

Update these to point to the KML you want to read in, and the KML you want the script to print out