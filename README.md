# Disease Detection in Crops

This project works with the help of Inceptionv3 Convolutional Neural Network (CNN) to detect disease from a crop image. The training of this CNN has been done on top of EPFL university's openly available dataset of crop images tagged with metadata such as crop name, disease and some more keywords.

### How to use this API

```python
import requests, json

def fetch_data_from_url(sample_image_url)  
    endpoint = "http://disection.herokuapp.com/disease_check"
    r = requests.post(endpoint, {"image_url": sample_image_url})
    content = r.content
    response = json.loads(str.encode("utf-8").strip())['data']
    return(response)

sample_image_url = "https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Apple___healthy/011d02f3-5c3c-4484-a384-b1a0a0dbdec1___RS_HL%207544.JPG"
fetch_data_from_url(sample_image_url)
#=> [{u'score': u'93.96', u'disease': u'healthy apple'}, {u'score': u'5.98', u'disease': u'apple scab'}, {u'score': u'0.06', u'disease': u'apple black rot'}, {u'score': u'0.0', u'disease': u'cedar apple rust'}]
```
