from django.db import models
from django.utils import timezone


class Upload(models.Model):
    title = models.CharField(max_length=120)
    document_url = models.URLField()
    created_at = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "{0} {1} {2} {3}".format(
            self, self.title, self.document_url, self.created_at)

    def publish(self):
        self.created_at = timezone.now()
        self.save()


class User(models.Model):
    upload_id = models.IntegerField()
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __unicode__(self):
        return "{0} {1} {2} {3} {4} {5} {6}".format(
            self, self.upload_id, self.first_name, self.last_name, self.age, self.gender, self.address)

    def publish(self):
        self.save()

