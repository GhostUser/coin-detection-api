import requests
import json
import sys
import cv2 #for output

url="http://127.0.0.1:8000/coin_detect/"

image=cv2.imread(sys.argv[1])

pload={"image": open("test_images\coin16.jpg", "rb")}

r=requests.post(url, files=pload).json()

print(f"Test Image: {r}")

for (x,y,r) in r["coins(x,y,r)"]:
        image=cv2.circle(image, (x,y), r, (0,0, 255),9)
        image=cv2.circle(image, (x,y), 10, (0,255,0), -1)
cv2.imshow("Detected Coins", image)
img_to_show=cv2.resize(image, (1000, 750))
cv2.imshow("Detected Coins", img_to_show)
cv2.waitKey(0)