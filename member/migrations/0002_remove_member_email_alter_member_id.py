# Generated by Django 5.0.4 on 2024-04-14 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='email',
        ),
        migrations.AlterField(
            model_name='member',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
