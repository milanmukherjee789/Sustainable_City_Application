from sklearn.datasets import load_sample_images
import cv2 as cv  # Imports OpenCV
import numpy as np
import requests
from PIL import Image
from flask import Flask, jsonify
import json
import csv

def get_cars(id):
    #Using OpenCV to to check the traffic
    goodImages = ''
    with open('./serverApi/csv_files/cctv.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # check if the ID of the current row matches the search ID
            if row['id'] == id:
                # if it does, print the data for that row
                goodImages = row['Link']
                break
    json_list = []
    #Get the image and resize
    image = Image.open(requests.get(goodImages, stream=True).raw)
    image = image.resize((450,250))
    image_arr = np.array(image)
    #Change the color of the image to grey
    grey = cv.cvtColor(image_arr, cv.COLOR_BGR2GRAY)
    Image.fromarray(grey)
    #Make the image blur
    blur = cv.GaussianBlur(grey,(5,5),0)
    Image.fromarray(blur)
    #Dilated the image
    dilated = cv.dilate(blur,np.ones((3,3)))
    Image.fromarray(dilated)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(2,2))
    closing = cv.morphologyEx(dilated, cv.MORPH_CLOSE, kernel)
    Image.fromarray(closing)
    #Load the car cascade classifier
    car_cascade_src = './serverApi/csv_files/cars.xml'
    car_cascade = cv.CascadeClassifier(car_cascade_src)
    traffic_classification = ""
    cars = car_cascade.detectMultiScale(closing,1.1,1)
    location_number = id
    #Detect the number of Cars
    cnt = 0
    for (x,y,w,h) in cars:
        cv.rectangle(image_arr,(x,y),(x+w,y+h),(255,0,0),2)
        cnt += 1
    if cnt >= 5:
        traffic_classification = "Traffic jam"
    elif cnt <= 4  and cnt > 0:
        traffic_classification = "Normal traffic"
    elif cnt == 0:
        traffic_classification = "No traffic"
    img = Image.fromarray(image_arr)
    result = '{ "location_number": "'+str(location_number)+'", "traffic_classification": "'+str(traffic_classification)+'",  "number_of_cars": "'+str(cnt)+'"}'
    return result

