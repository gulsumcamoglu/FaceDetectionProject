from django.db import models
import uuid


class reportModel(models.Model):
    TYPE_CHOICES = (
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly')
    )
    reportId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    typeReport = models.CharField(max_length=1,choices=TYPE_CHOICES)
    start = models.DateField(auto_now_add=False)
    end = models.DateField(auto_now_add=False)
    class Meta:
        db_table = 'report'
    def __str__(self):
        return str(self.typeReport)+" " + str(self.start)+" "  + str(self.end)