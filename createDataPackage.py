import xml.etree.ElementTree as ET
import uuid
import os
import requests
import json


folder_structure = {}

def create_xml(protocol, alias, uid, address, port, rover_port, ignore_embedded_klv, buffer_size, timeout, rtsp_reliable, region):
    # Create the root element
    root = ET.Element("feed")

    # Create child elements and set their text content
    elements = {
        "protocol": protocol,
        "alias": alias,
        "uid": uid,
        "address": address,
        "port": port,
        "roverPort": rover_port,
        "ignoreEmbeddedKLV": ignore_embedded_klv,
        "buffer": buffer_size,
        "timeout": timeout,
        "rtspReliable": rtsp_reliable
    }

    for element_name, element_value in elements.items():
        element = ET.SubElement(root, element_name)
        element.text = str(element_value)

    # Get the current working directory
    root_directory = os.getcwd()
   
    # Create a folder with the name of the region
    folder_name = region
    
    if region in folder_structure:
        folder_structure[region].append(uid)
    else:    
        folder_structure[region] = []
    
    # Construct the path to the folder
    folder_path = os.path.join(root_directory, folder_name)

    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If the folder doesn't exist, create it
        os.makedirs(folder_path)

    # Change the current working directory to the folder
    os.chdir(folder_path)
    print(f"Current working directory: {os.getcwd()}")

    # Create the XML tree
    tree = ET.ElementTree(root)
    os.makedirs(uid, exist_ok=True)

    filename = os.path.join(uid, f"{uid}.xml")
    # Save the XML to a file
    tree.write(filename, xml_declaration=True, encoding='UTF-8')

    # Return to the root directory
    os.chdir(root_directory)


def create_point_element(lat, lon, hae, ce, le):
    return ET.Element("point", lat=lat, lon=lon, hae=hae, ce=ce, le=le)

def create_sensor_element(vfov, elevation, fovBlue, fovRed, strokeWeight, roll, range_val, azimuth,
                          rangeLineStrokeWeight, fov, hideFov, rangeLineStrokeColor, fovGreen,
                          displayMagneticReference, strokeColor, rangeLines, fovAlpha):
    sensor = ET.Element("sensor", vfov=vfov, elevation=elevation, fovBlue=fovBlue, fovRed=fovRed,
                        strokeWeight=strokeWeight, roll=roll, range=range_val, azimuth=azimuth,
                        rangeLineStrokeWeight=rangeLineStrokeWeight, fov=fov, hideFov=hideFov,
                        rangeLineStrokeColor=rangeLineStrokeColor, fovGreen=fovGreen,
                        displayMagneticReference=displayMagneticReference, strokeColor=strokeColor,
                        rangeLines=rangeLines, fovAlpha=fovAlpha)
    return sensor

def create_link_element(uid, production_time, link_type, parent_callsign, relation):
    return ET.Element("link", uid=uid, production_time=production_time, type=link_type,
                      parent_callsign=parent_callsign, relation=relation)

def create_contact_element(callsign):
    return ET.Element("contact", callsign=callsign)

def create_color_element(argb):
    return ET.Element("color", argb=argb)

def create_video_element(uid, url):
    video = ET.Element("__video", uid=uid, url=url)
    return video

def create_connection_entry_element(networkTimeout, uid, path, protocol, bufferTime, address, port, roverPort,
                                    rtspReliable, ignoreEmbeddedKLV, alias):
    connection_entry = ET.Element("ConnectionEntry", networkTimeout=networkTimeout, uid=uid, path=path,
                                  protocol=protocol, bufferTime=bufferTime, address=address, port=port,
                                  roverPort=roverPort, rtspReliable=rtspReliable,
                                  ignoreEmbeddedKLV=ignoreEmbeddedKLV, alias=alias)
    return connection_entry

def create_remarks_element():
    remarks = ET.Element("remarks")
    return remarks

def create_event_xml(event_info, point_info, sensor_info, link_info, contact_info, color_info,
                     video_info, connection_entry_info, remarks_text, region):
    # Generate a UUID if not provided
    uid = event_info.get("uid", str(uuid.uuid4()))

    # Create the root element
    root = ET.Element("event", **event_info)

    # Create the 'point' element
    point = create_point_element(**point_info)
    root.append(point)

    # Create the 'detail' element
    detail = ET.SubElement(root, "detail")

    # Create child elements within the 'detail' element
    status = ET.SubElement(detail, "status", readiness=sensor_info.get("readiness", "true"))
    archive1 = ET.SubElement(detail, "archive")
    precision_location = ET.SubElement(detail, "precisionlocation", altsrc=sensor_info.get("altsrc", ""))
    
    # Create the 'sensor' element
    sensor = create_sensor_element(**sensor_info)
    detail.append(sensor)
    
    archive2 = ET.SubElement(detail, "archive")
    
    # Create the 'link' element
    link = create_link_element(**link_info)
    detail.append(link)
    
    # Create the 'contact' element
    contact = create_contact_element(**contact_info)
    detail.append(contact)
    
    # Create the 'color' element
    color = create_color_element(**color_info)
    detail.append(color)

    # Create the '__video' element
    video = create_video_element(**video_info)

    # Create the 'ConnectionEntry' element within '__video'
    connection_entry = create_connection_entry_element(**connection_entry_info)
    video.append(connection_entry)
    detail.append(video)

    # Create the 'remarks' element
    remarks = create_remarks_element()
    detail.append(remarks)

    # Create a folder with the name of the UUID
    folder_name = region
    if region in folder_structure:
        folder_structure[region].append(uid)
    else:    
        folder_structure[region] = []
    # Get the current working directory
    root_directory = os.getcwd()

    # Construct the path to the folder
    folder_path = os.path.join(root_directory, folder_name)

    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If the folder doesn't exist, create it
        os.makedirs(folder_path)

    # Change the current working directory to the folder
    os.chdir(folder_path)
    print(f"Current working directory: {os.getcwd()}")
    os.makedirs(uid, exist_ok=True)
    # Create the XML tree
    tree = ET.ElementTree(root)
    filename = os.path.join(uid, f"{uid}.cot")
    tree.write(filename, xml_declaration=True, encoding='UTF-8')

    # Return to the root directory
    os.chdir(root_directory)


def generate_manifest_xml(uid, name, contents):
    for city, uuid_list in folder_structure.items():    
        # Get the current working directory
        root_directory = os.getcwd()

        if city:
            # Construct the path to the folder
            folder_path = os.path.join(root_directory, str(city))
            os.chdir(folder_path)
        # Create the root element
        root = ET.Element("MissionPackageManifest", version="2")

        # Create the 'Configuration' element
        configuration = ET.SubElement(root, "Configuration")

        # Create 'Parameter' elements within 'Configuration'
        parameter_uid = ET.SubElement(configuration, "Parameter", name="uid", value=uid)
        parameter_name = ET.SubElement(configuration, "Parameter", name="name", value=name)

        # Create the 'Contents' element
        contents_element = ET.SubElement(root, "Contents")

        # Create 'Content' elements within 'Contents'
        for content in contents:
            for uuid in uuid_list:
                content_element = ET.SubElement(contents_element, "Content", ignore="false", zipEntry=content['zipEntry'])
                
                if content['uid'] == uuid:
                    # Create 'Parameter' elements within 'Content'
                    parameter_uid = ET.SubElement(content_element, "Parameter", name="uid", value=uuid)
                    parameter_name = ET.SubElement(content_element, "Parameter", name="name", value=content['name'])
                
                    if 'contentType' in content:
                        parameter_content_type = ET.SubElement(content_element, "Parameter", name="contentType", value=content['contentType'])

        # Create the XML tree
        tree = ET.ElementTree(root)

        # Save the XML to a file
        tree.write("manifest.xml", xml_declaration=True, encoding='UTF-8')
        os.chdir(root_directory)
    
def get_regions():
    url = 'https://chart.maryland.gov/DataFeeds/GetCamerasJson'
    response = requests.get(url)
    return json.loads(response.text)

def count_decimal_places(number):
    # Convert the float to a string
    number_str = str(number)

    # Check if the string contains a decimal point
    if '.' in number_str:
        # Get the substring after the decimal point and count its length
        decimal_places = len(number_str.split('.')[1])
        return decimal_places
    else:
        # If there is no decimal point, there are zero decimal places
        return 0

content = get_regions()
contents_info = []
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

for placemark in placemark_elements:
    hlsurl_element = placemark.find('.//kml:SimpleData[@name="hlsurl"]', namespaces=namespace)
    location_element = placemark.find('.//kml:SimpleData[@name="location"]', namespaces=namespace)
    lat_element = placemark.find('.//kml:SimpleData[@name="Latitude"]', namespaces=namespace)
    lon_element = placemark.find('.//kml:SimpleData[@name="Longitude"]', namespaces=namespace)
    if location_element is not None:
        location_value = location_element.text
        sensorUid = str(uuid.uuid4())
        videoUid = str(uuid.uuid4())
                
        event_info = {"version": "2.0", "uid": sensorUid , "type": "b-m-p-s-p-loc",
              "time": "2023-12-18T03:12:31.194Z", "start": "2023-12-18T03:12:31.194Z",
              "stale": "2024-12-17T03:12:31.194Z", "how": "h-g-i-g-o", "access": "Undefined"}

        point_info = {"lat": lat_element.text, "lon": lon_element.text, "hae": "105.112", "ce": "9999999.0", "le": "9999999.0"}

        sensor_info = {"vfov": "45", "elevation": "0", "fovBlue": "1.0", "fovRed": "1.0", "strokeWeight": "0.0", "roll": "0",
                    "range_val": "100", "azimuth": "270", "rangeLineStrokeWeight": "0.0", "fov": "45", "hideFov": "true",
                    "rangeLineStrokeColor": "-16777216", "fovGreen": "1.0", "displayMagneticReference": "0",
                    "strokeColor": "-16777216", "rangeLines": "100", "fovAlpha": "0.2980392156862745"}

        link_info = {"uid": "ANDROID-f18b0c86a8c70bcf", "production_time": "2023-12-18T03:08:49.272Z",
                    "link_type": "a-f-G-U-C", "parent_callsign": "JULIET ROMEO", "relation": "p-p"}

        contact_info = {"callsign": location_value}

        color_info = {"argb": "-1"}

        video_info = {"uid": videoUid,
                    "url": hlsurl_element.text}

        connection_entry_info = {"networkTimeout": "12000", "uid": videoUid,
                                "path": "", "protocol": "raw", "bufferTime": "-1",
                                "address": hlsurl_element.text,
                                "port": "80", "roverPort": "-1", "rtspReliable": "0", "ignoreEmbeddedKLV": "false",
                                "alias": location_value}

        remarks_text = ""
        
        region = ""
        for cam in content:
            lat_number = count_decimal_places(float(cam['lat']))
            lon_number = count_decimal_places(float(cam['lon']))
            if round(float(lat_element.text),lat_number -1 ) == round(float(cam['lat']),lat_number -1) and round(float(lon_element.text),lon_number-1) == round(float(cam['lon']), lon_number -1):
                region = cam['cameraCategories'][0]
                break
                
        create_xml("raw", location_value, videoUid, hlsurl_element.text, -1, -1, False, -1, 1200, 0, region)
        sensor = {'uid': sensorUid, 'name': location_value, 'zipEntry': f'{sensorUid}/{sensorUid}.cot'}
        video =  {'uid': videoUid, 'name': location_value, 'zipEntry': f'{videoUid}/{videoUid}.xml', 'contentType': 'Video'}
        create_event_xml(event_info, point_info, sensor_info, link_info, contact_info,
                 color_info, video_info, connection_entry_info, remarks_text, region)
        contents_info.append(video)
        contents_info.append(sensor)

generate_manifest_xml(uid=str(uuid.uuid4()), name='DP-JULIET ROMEO', contents=contents_info)
