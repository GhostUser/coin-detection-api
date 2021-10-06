# Coin Detection API
 This API is created using OpenCV and Django. It uses The [Circle Hough Transform](https://en.wikipedia.org/wiki/Circle_Hough_Transform) technique to find the circles and marks the center and radius of each circle. 

 The API returns response in JSON format i.e. 

 ```Test Image: {'success': True, 'Number of Coins': 17, 'coins(x,y,r)': [[847, 2357, 185], [1367, 2361, 190], [2699, 1153, 226], [2001, 667, 220], [2229, 1235, 189], [1771, 1467, 181], [1409, 1931, 190], [2777, 2263, 202], [2459, 1819, 186], [1125, 793, 221], [1585, 1077, 188], [3037, 1657, 222], [1925, 1931, 188], [795, 1709, 182], [585, 1183, 183], [1275, 1459, 191], [1839, 2519, 185]]}```

 ## Requirements
 Libraries and frameowrks required for the API to run are:
 
 1. Django ```pip install django```
 2. OpenCV ```pip install OpenCV``` 

 ## Run
 To run the api on your local server, you need to install the requirements and run the following command by opening command line from the project directory.

 ```python manage.py runserver```

## Test
The API can be tested using curl or the included ```test_api.py``` file.

Using test_api.py also displays the result image. 
![Result image](/doc_image/Screenshot703.png)

Using curl we get the response in JSON.
![JSON Response](/doc_image/InkScreenshot705.jpg)

1. To test the API using included test_api python file, 
    * run the ```test_api.py``` with path to the image as second argument .i.e  
    ```python test_api.py [path_to_image]```

2. To test the file using curl, use the following command
    * ```curl -X POST -F image=@[path_to_image] "[api_endpoint**]"```

        ** For local server use "http://127.0.0.1:8000/coin_detect/"```


## TODO
Need to add some more funtionality.
Will add soon