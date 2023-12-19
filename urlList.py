import xml.etree.ElementTree as ET
import json

# Specify the path to the KML file
kml_file_path = "MarylandTrafficCameras.kml"

# Read the content of the KML file
with open(kml_file_path, "r") as file:
    xml_string = file.read()

# Parse the XML string
root = ET.fromstring(xml_string)

# Find all Placemark elements within the Folder
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
placemark_elements = root.findall('.//kml:Placemark', namespaces=namespace)


urlDict ={}

# Extract and update the "location" field in each Placemark
for placemark in placemark_elements:
    hlsurl_element = placemark.find('.//kml:SimpleData[@name="hlsurl"]', namespaces=namespace)
    location_element = placemark.find('.//kml:SimpleData[@name="location"]', namespaces=namespace)
    if location_element is not None:
        location_value = location_element.text
        urlDict[location_value] = hlsurl_element.text
    else:
        print("Location not found in one of the Placemarks.")

with open('urls.json', 'w') as file:
     file.write(json.dumps(urlDict)) # use `json.loads` to do the reverse