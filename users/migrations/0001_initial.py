# Generated by Django 3.0.4 on 2020-05-13 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Squadron',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homebase', models.CharField(choices=[('B1', 'Base1'), ('B4', 'Base4'), ('B6', 'Base6'), ('B8', 'Base8'), ('B10', 'Base10'), ('B25', 'Base25'), ('B28', 'Base28'), ('B30', 'Base30')], default='B1', max_length=3)),
                ('Squadron_number', models.CharField(default='000', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='OperationalUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('squadron', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Squadron')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
