# Generated by Django 3.2.4 on 2021-07-03 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(default=None, max_length=300)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Subasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=300)),
                ('categoria', models.CharField(choices=[('Tecnology', 'Tecnology'), ('Fashion', 'Fashion'), ('Beauty', 'Beauty'), ('Home', 'Home')], default='Hogar', max_length=20)),
                ('precioInicial', models.IntegerField()),
                ('imagen', models.ImageField(blank=True, upload_to='auctions/static')),
                ('estado', models.BooleanField(default=True)),
                ('comentarios', models.ManyToManyField(blank=True, related_name='subastasC', to='auctions.Comentario')),
                ('ofertas', models.ManyToManyField(blank=True, related_name='subastasO', to='auctions.Oferta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subastasU', to='auctions.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Seguimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subastas', models.ManyToManyField(blank=True, related_name='Seguimientos', to='auctions.Subasta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='oferta',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas', to='auctions.usuario'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentarios', to='auctions.usuario'),
        ),
    ]
