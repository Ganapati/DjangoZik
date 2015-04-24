from django.db import models


class RemoteInstance(models.Model):
    name = models.CharField(max_length=250)
    url = models.CharField(max_length=256, null=True)
    key = models.TextField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ApiKey(models.Model):
    name = models.CharField(max_length=250)
    key = models.TextField(null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
