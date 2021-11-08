# Generated by Django 3.2.4 on 2021-08-15 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_user_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='descripcion',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='profiles'),
        ),
    ]
