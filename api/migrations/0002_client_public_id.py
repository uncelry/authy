# Generated by Django 4.1.1 on 2022-09-15 21:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='public_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]