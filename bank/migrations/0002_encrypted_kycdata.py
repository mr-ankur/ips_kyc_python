# Generated by Django 2.0.5 on 2022-03-14 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='encrypted_kycdata',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('unid', models.CharField(max_length=300)),
                ('cid', models.CharField(max_length=300)),
                ('cname', models.CharField(max_length=300)),
                ('aadharorignal_data', models.CharField(max_length=300)),
                ('aadharencrypted_data', models.CharField(max_length=300)),
                ('bankname', models.CharField(max_length=300)),
                ('phash1', models.CharField(max_length=300)),
                ('newhash1', models.CharField(max_length=300)),
                ('atimestamp', models.CharField(max_length=300)),
            ],
        ),
    ]