# Generated by Django 3.1.6 on 2022-11-19 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20221119_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='last_history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rooms.group'),
        ),
    ]