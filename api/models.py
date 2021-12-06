from django.db import models

# Create your models here.
class StringCalculator(models.Model):
    strReq = models.CharField(max_length = 255)
    strRes = models.IntegerField(null = True)
    dtCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.strReq + '=>' + str(self.strRes))
