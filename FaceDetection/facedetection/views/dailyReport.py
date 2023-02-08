from django.shortcuts import render,redirect
from facedetection.models import reportModel,detectionModel
from django.core.paginator import Paginator
from django.contrib import messages
from facedetection.forms import LastActiveForm
from datetime import date
import time
def dailyReport(request):
    form = LastActiveForm()
    if request.method =='POST':
        form = LastActiveForm(request.POST)
        
        if form.is_valid():
            dateForm = form.cleaned_data.get('choose_day')
            
            r = reportModel.objects.all()
            report = ""
            
            for i in r:
                print(dateForm)
                print(i.start)
                exist = False
                if i.typeReport =='D' and i.start == dateForm:
                    report = i
                    exist = True
                    break
                else:
                    exist = False
                    
        if exist:
            detections = report.detection.all()
            
                
            return render(request,'pages/dailyReport.html',context={
                                'detections' : detections,
                                'form':form  
                                    })    
        else:
            context = {
                            'alert1':'no detection'        
                    }
            messages.add_message(request, messages.INFO, context['alert1'])
            return render(request,'pages/dailyReport.html',context={
                            
                            'form':form  
                                 })    

                
                
    
    
            
    context = {
                'form':form          
            }
    return render(request,'pages/dailyReport.html',context={
                
                'form':form  
            })