from django.shortcuts import render
from facedetection.models import detectionModel
from django.core.paginator import Paginator
def detections(request):
    detections = detectionModel.objects.all()
    query = request.GET.get('page') 
    paginator = Paginator(detections,2)


    return render(request,'pages/detections.html',context={
        'detections' : paginator.get_page(query)
    })