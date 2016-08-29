from django.db import models

class Site(models.Model):
    url = models.CharField(max_length=500)
    site_name = models.CharField(max_length=30)
    responsible_account = models.CharField(max_length=50)
    schedule = models.DurationField()
    last_status = models.SmallIntegerField()
    first_checked = models.DateTimeField(auto_now_add = True)
    last_checked = models.DateTimeField(auto_now = True)
    
    
class Error(models.Model):
    site_id = models.ForeignKey(Site, on_delete=models.CASCADE)
    error_timestamp = models.DateTimeField(auto_now = True)
    error_code = models.SmallIntegerField()
    
    
