# Generated by Django 3.2.8 on 2021-10-29 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EpicEvents', '0003_rename_data_updated_client_date_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='data_updated',
            new_name='date_updated',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='data_updated',
            new_name='date_updated',
        ),
    ]
