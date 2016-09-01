from django.db import models

class Site(models.Model):
    url = models.CharField(max_length=500)
    site_name = models.CharField(max_length=30)
    responsible_account = models.CharField(max_length=50, null=True, blank=True)
    schedule = models.DurationField()
    last_status = models.SmallIntegerField()
    first_checked = models.DateTimeField()
    last_checked = models.DateTimeField()
    def __str__(self):
        return self.site_name

class Error(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    error_timestamp = models.DateTimeField(auto_now = True)
    error_code = models.SmallIntegerField()
    def __str__(self):
        return self.site
        
class Submission(models.Model):
    url = models.URLField(max_length=500)
    site_name = models.CharField(max_length=30)
    responsible_account = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.site_name