# Generated by Django 3.2.4 on 2021-06-12 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='text',
            field=models.TextField(default='q', max_length=600),
            preserve_default=False,
        ),
    ]
