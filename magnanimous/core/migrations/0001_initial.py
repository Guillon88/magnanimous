# Generated by Django 2.2.6 on 2019-10-19 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('IP', 'Incendio Pequeño'), ('IM', 'Incendio Mediano'), ('IG', 'Incendio Grande')], default='IP', max_length=4)),
            ],
        ),
    ]