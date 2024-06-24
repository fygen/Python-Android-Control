from os import getcwd
import xml.etree.ElementTree as ET
from datetime import datetime
from ppadb.client import Client
from PIL import Image
import numpy

def getUIAndroid(device):
    """
    Get the android screen variables in xml format then copy them to computer
    
    `adb shell uiautomator dump`
    
    copy the xml file to computer 
    
    `adb pull sdcard/window_dump.xml .`

    Returns:
        XML: A file which has points to which is application is where

    """
    cwd = getcwd()+'window_dump.xml'
    device.shell('uiautomator dump')
    device.pull('sdcard/window_dump.xml',cwd)
    return cwd

def saveScreen():    
    adb = Client (host='127.0.0.1',port=5037 )
    devices = adb.devices()
    if len(devices) == 0:
        print ('no device attached')
        quit()

    print( str(devices[0]))
    device = devices[0]
    image = device.screencap()

    timestamp = str(datetime.now()).replace(" ","").replace(":","").replace(".","")
    print(timestamp)
    picFile = 'aa.png' ## giveName
    with open(picFile, 'wb') as f:
        f.write(image)
    return device, image, picFile

def getXMLdata(fileName):
    """
    Read the contents of the XML file which returned from android
    Returns:

    """
    tree = ET.parse(fileName)
    root = tree.getroot()

    clickable_nodes = []
    for item in root.findall(".//node[@clickable='true']"):
        clickable_nodes.append(item)

    print(clickable_nodes) 
    return clickable_nodes


def print_clickable_nodes(clickable_nodes):
    """
    Prints the values of each clickable node.

    Parameters:
    clickable_nodes (List[ET.Element]): A list of XML elements with the attribute clickable="true".
    """
    for node in clickable_nodes:
        print("Node:")
        for attr, value in node.attrib.items():
            print(f"  {attr}: {value}")
        if node.text and node.text.strip():
            print(f"  Text: {node.text.strip()}")
        print()


def swipeScreen(device,xStart,xEnd,yStart,yEnd, distance):
    device.shell(f'input touchscreen swipe {xStart} {xEnd} {yStart} {yEnd} {int(distance)}')

device, image, picFile = saveScreen()
xmlfile = getUIAndroid(device)
clickable_nodes = getXMLdata(xmlfile)
print_clickable_nodes(clickable_nodes)
swipeScreen(device,500,500,750,1250,1000)