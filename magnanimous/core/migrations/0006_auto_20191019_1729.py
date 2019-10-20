# Generated by Django 2.2.6 on 2019-10-19 20:29

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import stream_django.activity


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0005_auto_20191019_1544'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('pin_count', models.IntegerField(default=0)),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(choices=[('IP', 'Incendio Pequeño'), ('IM', 'Incendio Mediano'), ('IG', 'Incendio Grande')], default='IP', max_length=4)),
                ('mpoly', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, stream_django.activity.Activity),
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('influencer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='influenced_pins', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(stream_django.activity.Activity, models.Model),
        ),
        migrations.DeleteModel(
            name='Evento',
        ),
    ]
