from django.db import models

class Sign(models.Model):
    name = models.CharField(max_length=20)
    phone = models.IntegerField()
    mail = models.EmailField()
    password = models.CharField(max_length=6)
    
    class Meta:
        db_table = 'sign_up'

class Storage(models.Model):
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=50,null=False,blank=False)
    body = models.TextField()

    class Meta:
        db_table = 'storage'