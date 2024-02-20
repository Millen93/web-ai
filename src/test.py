import requests 
import os 

image_file='./image.png'

with open(image_file, "rb") as f:
    im_bytes = f.read()

url = 'http://127.0.0.1:7000'



requests.post(url, files=im_bytes)
