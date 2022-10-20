from django.db import models
from picklefield.fields import PickledObjectField

# Create your models here.
class demoModel(models.Model):
    crds = PickledObjectField()