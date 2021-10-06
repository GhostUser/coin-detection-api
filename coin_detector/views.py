from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
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
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smooth_gray=cv2.medianBlur(gray, 3)

    cann=cv2.Canny(smooth_gray, 70, 140)

    thres=cv2.threshold(cann, 130, 255, cv2.THRESH_TRUNC)[1]


    circles=cv2.HoughCircles(thres,  cv2.HOUGH_GRADIENT, dp=2 ,minDist=425, minRadius=150, maxRadius=400)
    #Using Hough Circles to detect circles 
    circles=np.uint16(np.around(circles))
    circles=np.uint16(np.around(circles))

    print(f"No. of Coins: {len(circles[0, :])}")
    coin_det_list=[(int(i[0]), int(i[1]), int(i[2])) for i in circles[0, :]]
    #no_img=1
    #coin_det={}
    #coin_det_list=[]
  
    #for i in circles[0, :]:
        #for drawing circles
        #test_img2=cv2.circle(test_img2, (i[0], i[1]), i[2], (0,0, 255),9)
        #test_img2=cv2.circle(test_img2, (i[0], i[1]), 10, (0,255,0), -1)
        #print(f"Center: ({i[0]}, {i[1]}), Radius: {i[2]}")
        #coin_det_list+=[(i[0], i[1], i[2])]
        #coin_det[f"Coin {no_img}"]= f"Center: ({i[0]}, {i[1]}), Radius: {i[2]}"
        #no_img+=1

    #Dumping coin data into json
    data.update({"Number of Coins": len(circles[0, :]), "coins(x,y,r)": coin_det_list, "success": True})
    return JsonResponse(data)

def _grab_image(path=None, stream=None, url=None):
    if path is not None:
        image = cv2.imread(path)
    else:	
        if url is not None:
            resp = urllib.urlopen(url)
            data = resp.read()
        elif stream is not None:
            data = stream.read()
        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

class HomePageView(TemplateView):
    template_name = 'home.html'