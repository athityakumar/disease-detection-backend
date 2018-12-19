# Disease Detection in Crops

This project works with the help of Inceptionv3 Convolutional Neural Network (CNN) to detect disease from a crop image. The training of this CNN has been done on top of EPFL university's openly available dataset of crop images tagged with metadata such as crop name, disease and some more keywords.

### How to use this API

```python
import requests

endpoint = "http://disection.herokuapp.com/disease_check"
sample_image_url = "https://raw.githubusercontent.com/spMohanty/PlantVillage-Dataset/master/raw/color/Apple___healthy/011d02f3-5c3c-4484-a384-b1a0a0dbdec1___RS_HL%207544.JPG"

r = requests.post(endpoint, {"image_url": sample_image_url})
r.content

#=> '{"data":[{"disease":"healthy apple","score":"93.96"},{"disease":"apple scab","score":"5.98"},{"disease":"apple black rot","score":"0.06"},{"disease":"cedar apple rust","score":"0.0"}],"status":1}\n'
```
