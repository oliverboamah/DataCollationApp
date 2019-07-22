from django.db import models
from django.utils import timezone


# A table to hold upload/submission metadata
class Upload(models.Model):

    # table columns
    title = models.CharField(max_length=120)
    document_url = models.URLField()
    created_at = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "{0} {1} {2} {3}".format(
            self, self.title, self.document_url, self.created_at)

    # record current datetime before saving
    def publish(self):
        self.created_at = timezone.now()
        self.save()


# A table to hold the individual personal records
class User(models.Model):

    # table columns
    upload_id = models.IntegerField()
    first_name = models.CharField(max_length=120, null=True)
    last_name = models.CharField(max_length=120, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return "{0} {1} {2} {3} {4} {5} {6}".format(
            self, self.upload_id, self.first_name, self.last_name, self.age, self.gender, self.address)

    # save changes
    def publish(self):
        self.save()
