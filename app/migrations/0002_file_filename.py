# Generated by Django 2.2.5 on 2019-09-07 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='filename',
            field=models.CharField(default='default', max_length=256),
            preserve_default=False,
        ),
    ]
