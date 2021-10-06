from django.shortcuts import render
#importing libs
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
#for image processing
import numpy as np
import cv2
import json
import urllib

@csrf_exempt
def coin_detect(request):
    data = {"success": False}
    if request.method == "POST":
        if request.FILES.get("image", None) is not None:
            img = _grab_image(stream=request.FILES["image"])
        else:
            url = request.POST.get("url", None)
            if url is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)            
            img = _grab_image(url=url)
    #Coverting image to grayscale and applying threshold.
    img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(img.shape)
    ca=100
    cb=200
    ret, thres_tz= cv2.threshold(img_gray, 120, 255, cv2.THRESH_TOZERO)
    blur_tz=cv2.medianBlur(thres_tz, 5, 0)
    canny_tz=cv2.Canny(blur_tz, ca, cb)
    canny_tz_1=cv2.threshold(canny_tz, 100, 255, cv2.THRESH_BINARY)[1]

    #As a safe measure, copying the threshold and image to test_img
    test_img=canny_tz_1.copy()
    test_img2=img.copy()

    #Using Hough Circles to detect circles 
    circles=cv2.HoughCircles(test_img,  cv2.HOUGH_GRADIENT, dp=2 ,minDist=250, minRadius=150, maxRadius=300)
    circles=np.uint16(np.around(circles))

    print(f"No. of Coins: {len(circles[0, :])}")
    no_img=1
    coin_det={}
    for i in circles[0, :]:
        test_img2=cv2.circle(test_img2, (i[0], i[1]), i[2], (255,0,0),9)
        test_img2=cv2.circle(test_img2, (i[0], i[1]), 10, (0,0,255), -1)
        print(f"Center: ({i[0]}, {i[1]}), Radius: {i[2]}")
        coin_det[f"Coin {no_img}"]= f"Center: ({i[0]}, {i[1]}), Radius: {i[2]}"
        no_img+=1
    #Dumping coin dat into json
    data.update({"Number of Coins": len(circles[0, :]), "faces": coin_det, "success": True})
    return JsonResponse(data)

def _grab_image(path=None, url=None):
    if path is not None:
        image = cv2.imread(path)
    else:	
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()
        #converting file to numpy array and decoding into a image using open-CV
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image