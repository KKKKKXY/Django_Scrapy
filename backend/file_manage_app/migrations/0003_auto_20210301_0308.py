# Generated by Django 3.1.5 on 2021-03-01 03:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_manage_app', '0002_auto_20210224_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='filename',
            new_name='file_type',
        ),
    ]
