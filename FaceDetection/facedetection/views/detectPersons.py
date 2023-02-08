from django.http import HttpResponse
from facedetection.models import detectionModel,reportModel
from django.shortcuts import render,redirect,get_object_or_404
import os
import time
import uuid
import cv2
from tensorflow.keras.models import load_model
import tensorflow as tf
import json
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import argparse
import imutils
from datetime import date
import time
from datetime import datetime
import calendar
import pendulum

def detectPersons(request):
    
    if request.method =='POST':
        
        
        id,name,day,time,forName1,forName = takeImage()
        detection = detectionModel()
            
        detection.name = name
        detection.id = id
        detection.date = day
        detection.time =time
        detection.image = os.path.join('C:/Users/acer/Desktop/FaceDetection/media/uploads/'+str(name)+'.'+str(id)+'.'+str(forName1)+'.'+str(forName)+'.jpg')
        detection.save()
        reportsDaily = reportModel.objects.filter(typeReport = 'D')
            
        reportOuther = ""
        if len(reportsDaily) !=0:
            created = False
            for i in reportsDaily:
                print(detection.date)
                print(i.date)
                if i.date == detection.date:
                
                    created = True
                    report = i
                    break
                else:
                    created = False
            if created:
                    
                detection.reports.add(report)
            else:
                reportInner = reportModel()
                reportInner.typeReport = "D"
                reportInner.date = day
                reportInner.time =time
                d = datetime.strptime(day, "%d/%m/%Y").strftime("%Y-%m-%d")
                reportInner.start = d
                reportInner.end = d
                reportInner.save()
                reportOuther = reportInner
                detection.reports.add(reportOuther)
        else:
            reportInner = reportModel()
            reportInner.typeReport = "D"
            reportInner.date = day
            reportInner.time =time
            d = datetime.strptime(day, "%d/%m/%Y").strftime("%Y-%m-%d")
            reportInner.start = d
            reportInner.end = d
            reportInner.save()
            reportOuther = reportInner
            detection.reports.add(reportOuther)
        reportsWeekly = queryW()
            
            #if reportsWeekly == '':
        reportOuther = ""
        dt = datetime.now()
        print(dt.weekday())  
        if reportsWeekly:
            created = False
            for i in reportsWeekly:
                d1 = i.start
                d2 = detection.date
                d3 = i.end
                if d2>d1 and d2<d3:
                
                    created = True
                    report = i
                    break
                else:
                    created = False
            if created:
                detection.reports.add(report)
            else:
                if dt.weekday() == 0:
                    today = pendulum.now()
                    start = today.start_of('week')
                    start = start.to_datetime_string()[0:10]
                    end = today.end_of('week')
                    end = end.to_datetime_string()[0:10]
                    reportInner = reportModel()
                    reportInner.typeReport = "W"
                    reportInner.date = day
                    reportInner.start = start
                    reportInner.end = end
                        
                    reportInner.time =time
                    reportInner.save()
                    reportOuther = reportInner
                    detection.reports.add(reportOuther)
                else:
                    today = pendulum.now()
                    start = today.start_of('week')
                    start = start.to_datetime_string()[0:10]
                    end = today.end_of('week')
                    end = end.to_datetime_string()[0:10]
                    reportInner = reportModel()
                    reportInner.typeReport = "W"
                    reportInner.date = start
                    reportInner.start = start
                    reportInner.end = end
                        
                    reportInner.time =time
                    reportInner.save()
                    reportOuther = reportInner
                    detection.reports.add(reportOuther)

        else:
            if dt.weekday() == 0:
                reportInner = reportModel()
                reportInner.typeReport = "W"
                reportInner.date = day
                reportInner.time =time
                reportInner.save()
                reportOuther = reportInner
                detection.reports.add(reportOuther)
            else:
                today = pendulum.now()
                start = today.start_of('week')
                start = start.to_datetime_string()[0:10]
                end = today.end_of('week')
                end = end.to_datetime_string()[0:10]
                reportInner = reportModel()
                reportInner.typeReport = "W"
                reportInner.date = start
                reportInner.start = start
                reportInner.end = end
                        
                reportInner.time =time
                reportInner.save()
                reportOuther = reportInner
                detection.reports.add(reportOuther)

        reportsMonthly = queryM()
            
            #if reportsWeekly == '':
        reportOuther = ""
        if reportsMonthly:
            created = False
            for i in reportsMonthly:
                today = pendulum.now()
                print(today)
                print(today.to_datetime_string()[5:7])    
                if i.start.strftime("%Y/%m") == detection.date.strftime("%Y/%m"):
                
                    created = True
                    report = i
                    break
                else:
                    created = False
            if created:
                    
                detection.reports.add(report)
            else:
                input_dt = datetime.today()
                res = input_dt.replace(day=1)
                today = pendulum.now()
                start = today.start_of('week')
                start = start.to_datetime_string()[0:10]
                end = today.end_of('week')
                end = end.to_datetime_string()[0:10]
                reportInner = reportModel()
                reportInner.typeReport = "M"
                reportInner.date = day
                reportInner.time =time
                reportInner.start = start
                reportInner.end = end
                reportInner.save()
                reportOuther = reportInner
                detection.reports.add(reportOuther)
        else:
            input_dt = datetime.today()
            res = input_dt.replace(day=1)
            res2 = input_dt.replace(day=31)
            
            
            reportInner = reportModel()
            reportInner.typeReport = "M"
            reportInner.date = res
            reportInner.time =time
            reportInner.start = res
            reportInner.end = res2
            reportInner.save()
            reportOuther = reportInner
            detection.reports.add(reportOuther)
            
            

                        
                

        
        return redirect('detectPersons') 
    
    return render(request,'pages/detectPerson.html',context={})
def queryW():
    try:
        return reportModel.objects.filter(typeReport = 'W')
    except reportModel.DoesNotExist:
        return False
def queryM():
    try:
        return reportModel.objects.filter(typeReport = 'M')
    except reportModel.DoesNotExist:
        return False
    
def takeImage():
    count = 0
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        facetracker = load_model('facedetection/facetracker.h5') 

        r = cv2.face.LBPHFaceRecognizer_create()
        r.read('facedetection\model.yml')
        path = os.path.join('C:/Users/acer/Desktop/FaceDetection/facedetection/names.json')
        if os.path.exists(path):
                  with open(path, 'r') as f:
                    namesJson = json.load(f)
        names = namesJson['name']
        idss = namesJson['id']
        _ , frame = cap.read()
        frame = frame[50:500, 50:500,:]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = tf.image.resize(rgb, (120,120))
        
        yhat = facetracker.predict(np.expand_dims(resized/255,0))
        sample_coords = yhat[1][0]
        print(np.multiply(sample_coords, [450,450,450,450]).astype(int))
        
        for [x,y,w,h] in [np.multiply(sample_coords, [450,450,450,450]).astype(int).tolist()]:
            
            if x > 10:
                id, confidence = r.predict(gray[y:h,x:w])
                idNum = id
                print(confidence)
                cv2.rectangle(frame, 
                            tuple(np.multiply(sample_coords[:2], [450,450]).astype(int)),
                            tuple(np.multiply(sample_coords[2:], [450,450]).astype(int)), 
                                    (255,0,0), 2)
                # Controls the label rectangle
                cv2.rectangle(frame, 
                            tuple(np.add(np.multiply(sample_coords[:2], [450,450]).astype(int), 
                                            [0,-30])),
                            tuple(np.add(np.multiply(sample_coords[:2], [450,450]).astype(int),
                                            [80,0])), 
                                    (255,0,0), -1)
                if  yhat[0] > 0.5  and confidence<100:
                    for i in idss:
                        if i == id:
                            index = idss.index(i)
                            break
                    id = names[index]
                # Controls the text rendered
                    cv2.putText(frame, str(id), tuple(np.add(np.multiply(sample_coords[:2], [450,450]).astype(int),
                            [0,-5])),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                else:
                    id = "unknown"
                    cv2.putText(frame, str(id), tuple(np.add(np.multiply(sample_coords[:2], [450,450]).astype(int),
                            [0,-5])),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            else:
                id = "no face"
                cv2.putText(frame, str(id), tuple(np.add(np.multiply(sample_coords[:2], [450,450]).astype(int),
                                [0,-5])),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        

        
        
        cv2.imshow('EyeTrack', frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
           
            break
            
            
        elif k%256 == 32:
            lastId = ""
            lastName = ""
            today = date.today() #for finding the day
            t = time.localtime() 
            d1 = today.strftime("%d/%m/%Y")
            current_time = time.strftime("%H:%M:%S", t)
            # SPACE pressed
            forName1 = today.strftime("%d%m%Y")
            forName = time.strftime("%H%M%S", t)
            file_name_path2 = 'C:/Users/acer/Desktop/FaceDetection/media/uploads/'+str(id)+'.'+str(idNum)+'.'+str(forName1)+'.'+str(forName)+'.jpg'
            lastId= idNum
            lastName = id
            
            cv2.imwrite(file_name_path2, frame)
            print("{} written!".format(file_name_path2))
            
            cap.release()
            cv2.destroyAllWindows()
            return lastId,lastName,d1,current_time,forName1,forName
    
    
    
        

    


