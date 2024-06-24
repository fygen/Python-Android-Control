import xml.etree.ElementTree as ET
from datetime import datetime
from ppadb.client import Client
from PIL import Image
import numpy, time


def swipeScreen(device,xStart,xEnd,yStart,yEnd, distance):
    device.shell(f'input touchscreen swipe {xStart} {xEnd} {yStart} {yEnd} {int(distance)}')

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


def getUIAndroid():
    """
    Get the android screen variables in xml format then copy them to computer
    
    `adb shell uiautomator dump`
    
    copy the xml file to computer 
    
    `adb pull sdcard/window_dump.xml .`

    Returns:
        XML: A file which has points to which is application is where

    """
    print(NotImplemented)

def giveName():
    """
    Generates a filename based on the current timestamp.
    
    Returns:
        str: A string in the format 'screen-{timestamp}.png'
    """
    return f'Screen-{timestamp}.png'

def categorize_color(r, g, b):
    """
    Categorizes the given RGB values into color categories based on human perception.
    
    Parameters:
        r (int): Red component (0-255).
        g (int): Green component (0-255).
        b (int): Blue component (0-255).
        
    Returns:
        str: A string indicating the color category ('yellow', 'black', 'green', etc.).
    """
    # Calculate brightness (luminance) based on RGB values
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    # Define thresholds based on human perception
    if brightness > 0.9:
        return "white"
    elif brightness < 0.1:
        return "black"
    elif r > g and r > b:
        return "red"
    elif g > r and g > b:
        return "green"
    elif b > r and b > g:
        return "blue"
    elif r > 150 and g > 150 and b < 75:
        return "yellow"
    elif r > 150 and g < 75 and b < 75:
        return "orange"
    elif r < 100 and g > 100 and b < 100:
        return "purple"
    else:
        return "unknown"

adb = Client (host='127.0.0.1',port=5037 )
devices = adb.devices()
if len(devices) == 0:
    print ('no device attached')
    quit()

print( str(devices[0]))
device = devices[0]
while True:
    image = device.screencap()

    timestamp = str(datetime.now()).replace(" ","").replace(":","").replace(".","")
    print(timestamp)
    picFile = 'aa.png' ## giveName()
    with open(picFile, 'wb') as f:
        f.write(image)

    image = Image.open(picFile)
    image = numpy.array(image, dtype=numpy.uint8)
    print(image.shape)

    pixels = [i[:3] for i in image[1747]]
    ignore = True
    black = True

    clickable_elements = getXMLdata("window_dump.xml")
    print_clickable_nodes(clickable_elements)

    lastColorOfIndex = 'unknown' 
    categorized = []
    ListOfBoundaries = []
    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]
        colorOfIndex = categorize_color(r,g,b)
        categorized.append([pixel, colorOfIndex])
        if lastColorOfIndex != colorOfIndex:
            if colorOfIndex != 'unknown':
                if i > 100:
                    ListOfBoundaries.append([i,colorOfIndex])
        lastColorOfIndex = colorOfIndex

    print(ListOfBoundaries)

    categorized_array = numpy.array(categorized, dtype=object)
    print(categorized_array.shape)
    print(categorized_array)

    lastboundary = [0, 'unknown']
    for i, boundary in enumerate(ListOfBoundaries):
        print ("i is: ", i)
        print(lastboundary[1], boundary[1], ListOfBoundaries[i+1][1] )
        if lastboundary[1] == 'black' and boundary[1] == 'red' and ListOfBoundaries[i+1][1] == 'black': 
                toIndex = boundary
                break
        lastboundary = boundary
    print(toIndex)

    swipeScreen(device,500,500,600,600, toIndex[0]-ListOfBoundaries[0][0])
    time.sleep(2)
    #   categorized[:][:][1])
    # if ignore and (r+g+b) != 0:
    #     continue

    # ignore = False


# print(pixels[100])

