# Generated by Django 3.2.4 on 2021-08-15 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_user_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='imagen',
            field=models.ImageField(null=True, upload_to='profiles'),
        ),
    ]
