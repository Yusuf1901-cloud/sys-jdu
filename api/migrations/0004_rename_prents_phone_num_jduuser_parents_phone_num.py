# Generated by Django 5.0.1 on 2024-01-23 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_parents_phone_num_jduuser_prents_phone_num'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jduuser',
            old_name='prents_phone_num',
            new_name='parents_phone_num',
        ),
    ]
