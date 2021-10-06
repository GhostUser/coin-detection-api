import requests
import json
import sys
import cv2 #for output

url="http://127.0.0.1:8000/coin_detect/"

image=cv2.imread(sys.argv[1])
test_img=image.copy()

pload={"image": open("test_images\coin16.jpg", "rb")}

r=requests.post(url, files=pload).json()

print(f"Test Image: {r}")

for (x,y,r) in r["coins(x,y,r)"]:
        test_img=cv2.circle(test_img, (x,y), r, (0,0, 255),9)
        test_img=cv2.circle(test_img, (x,y), 10, (0,255,0), -1)
cv2.imshow("Detected Coins", test_img)
img_to_show=cv2.resize(test_img, (1000, 750))
cv2.imshow("Detected Coins", img_to_show)
cv2.waitKey(0)