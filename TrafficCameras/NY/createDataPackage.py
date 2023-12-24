import xml.etree.ElementTree as ET
import uuid
import os
import requests
import json


folder_structure = {}

def folder_setup(uid, root, extension):
    # Get the current working directory
    root_directory = os.getcwd()
   
    folder_name= ""
    # Create a folder with the name of the region
    if region:
        folder_name = region
    else:
        folder_name = "ungrouped"
    
    if region in folder_structure:
        folder_structure[region].append(uid)
    else:    
        folder_structure[region] = []
        folder_structure[region].append(uid)

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

    filename = os.path.join(uid, f"{uid}.{extension}")
    # Save the XML to a file
    tree.write(filename, xml_declaration=True, encoding='UTF-8')

    # Return to the root directory
    os.chdir(root_directory)

def get_regions(request_url):
    response = requests.get(request_url)
    return json.loads(response.text)


def create_point_xml(protocol, alias, uid, address, port, rover_port, ignore_embedded_klv, buffer_size, timeout, rtsp_reliable, region):
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


    folder_setup(uid, root, "xml")
    


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
    ET.SubElement(detail, "archive")
    # Create the 'contact' element
    contact = create_contact_element(**contact_info)
    detail.append(contact)
    ET.SubElement(detail, "archive")
    # Create the 'remarks' element
    remarks = create_remarks_element()
    detail.append(remarks)
    # Create the 'link' element
    link = create_link_element(**link_info)
    detail.append(link)

    # Create the '__video' element
    video = create_video_element(**video_info)

    # Create the 'ConnectionEntry' element within '__video'
    connection_entry = create_connection_entry_element(**connection_entry_info)
    video.append(connection_entry)
    detail.append(video)

    ET.SubElement(detail, "precisionlocation", altsrc=sensor_info.get("altsrc", ""))
    
    # Create the 'sensor' element
    sensor = create_sensor_element(**sensor_info)
    detail.append(sensor)


    folder_setup(uid, root, "cot")


def generate_manifest_xml(contents):
    for city, uuid_list in folder_structure.items():    
        # Get the current working directory
        root_directory = os.getcwd()

        if city:
            # Construct the path to the folder
            folder_path = os.path.join(root_directory, str(city))
            os.chdir(folder_path)
        else:
            city = "ungrouped"
            folder_path = os.path.join(root_directory, "ungrouped")
            os.chdir(folder_path)

        os.mkdir('MANIFEST')
        os.chdir('MANIFEST')
        # Create the root element
        root = ET.Element("MissionPackageManifest", version="2")

        # Create the 'Configuration' element
        configuration = ET.SubElement(root, "Configuration")

        # Create 'Parameter' elements within 'Configuration'
        ET.SubElement(configuration, "Parameter", name="uid", value=str(uuid.uuid4()))
        ET.SubElement(configuration, "Parameter", name="name", value=f"{city}_traffic_cams")

        # Create the 'Contents' element
        contents_element = ET.SubElement(root, "Contents")

        # Create 'Content' elements within 'Contents'
        for content in contents:                
            if content['uid'] in uuid_list:
                content_element = ET.SubElement(contents_element, "Content", ignore="false", zipEntry=content['zipEntry'])
                if '.cot' in content['zipEntry']:
                    # Create 'Parameter' elements within 'Content'
                    ET.SubElement(content_element, "Parameter", name="uid", value=content['uid'])
                if '.xml' in content['zipEntry']:
                    ET.SubElement(content_element, "Parameter", name="name", value=content['name'])
                    
                    # if 'contentType' in content:
                    #     parameter_content_type = ET.SubElement(content_element, "Parameter", name="contentType", value=content['contentType'])

        # Create the XML tree
        tree = ET.ElementTree(root)

        # Save the XML to a file
        tree.write("manifest.xml", xml_declaration=True, encoding='UTF-8')
        os.chdir(root_directory)
    
def get_regions(request_url):
    response = requests.get(request_url)
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

content = get_regions("https://webcams.nyctmc.org/api/cameras")
contents_info = []
# Specify the path to the KML file
kml_file_path = "NYCDOT_TrafficCameras.kml"

# Read the content of the KML file
with open(kml_file_path, "r") as file:
    xml_string = file.read()

# Parse the XML string
sensor_root = ET.fromstring(xml_string)

# Find all Placemark elements within the Folder
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
placemark_elements = sensor_root.findall('.//kml:Placemark', namespaces=namespace)

    
for placemark in placemark_elements:
    url_element = placemark.find('.//kml:SimpleData[@name="URLIMAGE"]', namespaces=namespace)
    location_element = placemark.find('.//kml:SimpleData[@name="LOCATION"]', namespaces=namespace)
    lat_element = placemark.find('.//kml:SimpleData[@name="LAT"]', namespaces=namespace)
    lon_element = placemark.find('.//kml:SimpleData[@name="LON"]', namespaces=namespace)
    if location_element is not None:
        location_value = location_element.text
        sensorUid = str(uuid.uuid4())
        videoUid = str(uuid.uuid4())
                
        event_info = {"version": "2.0", "uid": sensorUid , "type": "b-m-p-s-p-loc",
              "time": "2023-12-18T03:12:31.194Z", "start": "2023-12-18T03:12:31.194Z",
              "stale": "2024-12-17T03:12:31.194Z", "how": "h-g-i-g-o"}

        point_info = {"lat": lat_element.text, "lon": lon_element.text, "hae": "105.112", "ce": "9999999.0", "le": "9999999.0"}

        sensor_info = {"vfov": "45", "elevation": "0", "fovBlue": "1.0", "fovRed": "1.0", "strokeWeight": "0.0", "roll": "0",
                    "range_val": "100", "azimuth": "270", "rangeLineStrokeWeight": "0.0", "fov": "45", "hideFov": "true",
                    "rangeLineStrokeColor": "-16777216", "fovGreen": "1.0", "displayMagneticReference": "0",
                    "strokeColor": "-16777216", "rangeLines": "100", "fovAlpha": "0.2980392156862745"}

        link_info = {"uid": "ANDROID-f18b0c86a8c70bcf", "production_time": "2023-12-18T03:08:49.272Z",
                    "link_type": "a-f-G-U-C", "parent_callsign": "ALPHA", "relation": "p-p"}

        contact_info = {"callsign": location_value}

        color_info = {"argb": "-1"}

        video_info = {"uid": videoUid,
                    "url": url_element.text}

        connection_entry_info = {"networkTimeout": "12000", "uid": videoUid,
                                "path": "", "protocol": "raw", "bufferTime": "-1",
                                "address": url_element.text,
                                "port": "80", "roverPort": "-1", "rtspReliable": "0", "ignoreEmbeddedKLV": "false",
                                "alias": location_value}

        remarks_text = ""
        
        region = ""
        for cam in content:
            lat_number = count_decimal_places(float(cam['latitude']))
            lon_number = count_decimal_places(float(cam['longitude']))
            if round(float(lat_element.text),lat_number -1 ) == round(float(cam['latitude']),lat_number -1) and round(float(lon_element.text),lon_number-1) == round(float(cam['longitude']), lon_number -1):
                region = cam['area']
                break
                
        create_event_xml(event_info, point_info, sensor_info, link_info, contact_info,
                 color_info, video_info, connection_entry_info, remarks_text, region)        
        create_point_xml("raw", location_value, videoUid, url_element.text, 80, -1, "false", -1, 1200, 0, region)
        sensor = {'uid': sensorUid, 'name': location_value, 'zipEntry': f'{sensorUid}/{sensorUid}.cot'}
        video =  {'uid': videoUid, 'name': location_value, 'zipEntry': f'{videoUid}/{videoUid}.xml', 'contentType': 'Video'}
        contents_info.append(sensor)
        contents_info.append(video)

generate_manifest_xml(contents=contents_info)
