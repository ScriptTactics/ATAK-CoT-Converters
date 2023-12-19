import xml.etree.ElementTree as ET

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

# Extract and update the "location" field in each Placemark
for placemark in placemark_elements:
    location_element = placemark.find('.//kml:SimpleData[@name="location"]', namespaces=namespace)
    if location_element is not None:
        location_value = location_element.text

        # Create a new <name> element
        name_element = ET.Element('name')
        name_element.text = location_value

        # Insert the <name> element after <Placemark> and before <ExtendedData>
        placemark.insert(0, name_element)
        print(f"Added <name>{location_value}</name> in one of the Placemarks.")
    else:
        print("Location not found in one of the Placemarks.")

# Save the modified XML to a new file or overwrite the original file
new_kml_file_path = "MarylandTrafficCameras_new.kml"
ET.ElementTree(root).write(new_kml_file_path, encoding="utf-8", xml_declaration=True)

print(f"Modified KML saved to: {new_kml_file_path}")
