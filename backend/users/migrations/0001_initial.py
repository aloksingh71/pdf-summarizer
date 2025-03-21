# Generated by Django 5.1.7 on 2025-03-18 21:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('file_name', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary_type', models.CharField(choices=[('bullet', 'Bullet'), ('paragraph', 'Paragraph')], max_length=20)),
                ('num_points', models.IntegerField(blank=True, null=True)),
                ('paragraph_length', models.IntegerField(blank=True, null=True)),
                ('summary_text', models.TextField()),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('uploaded_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.uploadedfile')),
            ],
        ),
    ]
