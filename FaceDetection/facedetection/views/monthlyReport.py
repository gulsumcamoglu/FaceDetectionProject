from django.shortcuts import render
from facedetection.models import reportModel,detectionModel
from django.core.paginator import Paginator
from facedetection.forms import LastActiveFormWeekly
from django.contrib import messages
import time
def monthlyReport(request):
    form = LastActiveFormWeekly()
    if request.method =='POST':
        form = LastActiveFormWeekly(request.POST)
        
        if form.is_valid():
            dateForm1 = form.cleaned_data.get('first_date')
            dateForm2 = form.cleaned_data.get('last_date')
            r = reportModel.objects.all()
            report = ""
            
            for i in r:
                print(dateForm1)
                print(dateForm2)
                print(i.start)
                exist = False
                if i.typeReport =='M' and i.start == dateForm1 and i.end == dateForm2:
                    report = i
                    exist = True
                    break
                else:
                    exist = False
                    
        if exist:
            detections = report.detection.all()
            
                
            return render(request,'pages/monthlyReport.html',context={
                                'detections' : detections,
                                'form':form  
                                    })    
        else:
            context = {
                            'alert1':'no detection'        
                    }
            messages.add_message(request, messages.INFO, context['alert1'])
            return render(request,'pages/monthlyReport.html',context={
                            
                            'form':form  
                                 })    

                
                
    
    
            
    context = {
                'form':form          
            }
    return render(request,'pages/monthlyReport.html',context={
                
                'form':form  
            })