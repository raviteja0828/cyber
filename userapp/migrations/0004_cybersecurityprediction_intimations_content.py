# Generated by Django 5.0.1 on 2025-02-28 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0003_cybersecurityprediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='cybersecurityprediction',
            name='intimations_content',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]
