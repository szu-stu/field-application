from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Document(models.Model):
    docfile = models.FileField(upload_to='documents')
    docname = models.CharField(max_length=50)

@receiver(post_delete, sender=Document)
def Document_delete(sender, instance, **kwargs):
    if instance.docfile:
        instance.docfile.delete(False)
