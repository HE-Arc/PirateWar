# Generated by Django 2.0.2 on 2018-03-28 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pirateWarApp', '0002_auto_20180326_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ship',
            name='currentActivity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pirateWarApp.Activity'),
        ),
    ]
