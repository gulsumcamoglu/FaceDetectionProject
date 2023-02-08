from django.db import models
import uuid
from facedetection.models import reportModel


class detectionModel(models.Model):
    detectionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='uploads')
    name = models.CharField(max_length=30,blank=False,null=False)
    id = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    reports = models.ManyToManyField(reportModel, related_name='detection') #bu report üzerinden bütün detectionlara erişmek için related name
    
    class Meta:
        db_table = 'detection'

    def __str__(self):
        return str(self.name)+" " + str(self.date)+" "  + str(self.time)