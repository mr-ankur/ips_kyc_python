from django.db import models

# Create your models here.
class customerreg(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    mobile = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    uname = models.CharField(max_length=300)
    password = models.CharField(max_length=300)

class upload_kyc(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.CharField(max_length=300)
    cname =  models.CharField(max_length=300)
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mobile = models.CharField(max_length=300)
    gender = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    bankname= models.CharField(max_length=300)
    banklocation= models.CharField(max_length=300)

class upload_kycdet(models.Model):
    id = models.AutoField(primary_key=True)
    cid = models.CharField(max_length=300)
    cname =  models.CharField(max_length=300)
    aadhar = models.FileField()
    voter_id = models.FileField()
    pan_card = models.FileField()
    status = models.CharField(max_length=300)
    bankname= models.CharField(max_length=300)
    banklocation= models.CharField(max_length=300)
