from django.db import models

# Create your models here.
class bankreg(models.Model):
    id = models.AutoField(primary_key=True)
    bankname = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    mobile = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    uname = models.CharField(max_length=300)
    password = models.CharField(max_length=300)

class encrypted_kycdata(models.Model):
    id = models.AutoField(primary_key=True)
    unid=models.CharField(max_length=300)
    cid = models.CharField(max_length=300)
    cname = models.CharField(max_length=300)
    aadharorignal_data = models.CharField(max_length=300)
    aadharencrypted_data = models.CharField(max_length=300)
    voterencrypted_data = models.CharField(max_length=300)
    panencrypted_data = models.CharField(max_length=300)
    bankname=models.CharField(max_length=300)
    phash1 = models.CharField(max_length=300)
    newhash1 = models.CharField(max_length=300)
    atimestamp = models.CharField(max_length=300)


class sharekey_request(models.Model):
    id = models.AutoField(primary_key=True)
    cid=models.CharField(max_length=300)
    cname = models.CharField(max_length=300)
    bankid = models.CharField(max_length=300)
    bankname = models.CharField(max_length=300)
    buname = models.CharField(max_length=300)
    bemail = models.CharField(max_length=300)
    hashvalue = models.CharField(max_length=300)
    status = models.CharField(max_length=300)

class pkey_request(models.Model):
    id = models.AutoField(primary_key=True)
    cid=models.CharField(max_length=300)
    cname = models.CharField(max_length=300)
    bankid = models.CharField(max_length=300)
    bankname = models.CharField(max_length=300)
    buname = models.CharField(max_length=300)
    bemail = models.CharField(max_length=300)
    pkey1 = models.CharField(max_length=300)
    status = models.CharField(max_length=300)


