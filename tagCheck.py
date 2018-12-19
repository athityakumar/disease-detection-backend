from __future__ import print_function
import time
import requests
import cv2
import operator
import numpy as np
from label_image import IMAGES_PATH, MODELS_PATH
# Import library to display results
import matplotlib.pyplot as plt

_url = 'https://api.projectoxford.ai/vision/v1.0/analyze'
# Here you have to paste your primary key
_key = '6d9c00fc83be42649e476783b5241e2e'
_maxNumRetries = 10

def processRequest(json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request(
            'post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else Nne
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result


def renderResultOnImage(result, img):
    flag = 1
    """Display the obtained results onto the input image"""
    R = int(result['color']['accentColor'][:2], 16)
    G = int(result['color']['accentColor'][2:4], 16)
    B = int(result['color']['accentColor'][4:], 16)

    cv2.rectangle(
        img, (0, 0), (img.shape[1], img.shape[0]), color=(R, G, B), thickness=25)

    for cat in result['categories']:
        if cat['name']=='plant_leaves':
            flag=0
            break

    return flag

# Via URL
'''
# URL direction to image
urlImage = 'https://oxfordportal.blob.core.windows.net/vision/Analysis/3.jpg'

# Computer Vision parameters
params = { 'visualFeatures' : 'Color,Categories'} 

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/json' 

json = { 'url': urlImage } 
data = None

result = processRequest( json, data, headers, params )

if result is not None:
    # Load the original image, fetched from the URL
    arr = np.asarray( bytearray( requests.get( urlImage ).content ), dtype=np.uint8 )
    img = cv2.cvtColor( cv2.imdecode( arr, -1 ), cv2.COLOR_BGR2RGB )

    renderResultOnImage( result, img )

    ig, ax = plt.subplots(figsize=(15, 20))
    ax.imshow( img )
'''

# Via Disk


def main(image_name):
    # Load raw image file into memory

    pathToFileInDisk = image_name
    with open(pathToFileInDisk, 'rb') as f:
        data = f.read()
        print(data)
    # Computer Vision parameters
    params = {'visualFeatures': 'Color,Categories'}

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None

    result = processRequest(json, data, headers, params)

    if result is not None:
        # Load the original image, fetched from the URL
        # Convert string to an unsigned int array
        data8uint = np.fromstring(data, np.uint8)
        img = cv2.cvtColor(
            cv2.imdecode(data8uint, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
        try :
            flagc = renderResultOnImage(result, img)
        except :
            flagc = 1
        if flagc == 1:
            print("Invalid Image! Try Again.")
            return False 
        else:
            print("Checking Disease")
            return True
            #ig, ax = plt.subplots(figsize=(15, 20))
            #ax.imshow(img)

if __name__ == '__main__':
    main()
