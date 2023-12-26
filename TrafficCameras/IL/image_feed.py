import xml.etree.ElementTree as ET

# Specify the path to the KML file
kml_file_path = "Illinois_Gateway_Traffic_Cameras.kml"

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
    location_element = placemark.find('.//kml:SimpleData[@name="CameraLocation"]', namespaces=namespace)
    snapshot_url = placemark.find('.//kml:SimpleData[@name="SnapShot"]', namespaces=namespace)
    if location_element is not None:
        location_value = location_element.text

        name_element = placemark.find('.//kml:name', namespaces=namespace)
        if name_element:
            name_element.text = location_value
        else:
            # Create a new <name> element
            name_element = ET.Element('name')
            name_element.text = location_value
            placemark.insert(0, name_element)
                # Insert the <name> element after <Placemark> and before <ExtendedData>
        print(f"Added <name>{location_value}</name> in one of the Placemarks.")
    else:
        print("Location not found in one of the Placemarks.")
    
    description_element = ET.Element('description')

    sub_description = ET.Element('description')
    text = '<![CDATA[<html><img src="' + snapshot_url.text + '"></img></html>]]>'
    sub_description.text = text
    description_element.append(sub_description)
        
    placemark.insert(1, description_element)
    print(f"Added <dscription>{description_element.text}</description> in one of the Placemarks.")


# Save the modified XML to a new file or overwrite the original file
new_kml_file_path = "Illinois_Gateway_Traffic_Cameras_new.kml"
ET.ElementTree(root).write(new_kml_file_path, encoding="utf-8", xml_declaration=True)

print(f"Modified KML saved to: {new_kml_file_path}")
