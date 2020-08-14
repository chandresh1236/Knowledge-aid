# Generated by Django 3.0.2 on 2020-08-10 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_delete_blogpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_name', models.CharField(max_length=20)),
                ('chapter_created_date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.course')),
            ],
        ),
        migrations.CreateModel(
            name='YTLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('yt_link_fk', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='TextBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('text_block_fk', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default='', upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('file_fk', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.Chapter')),
            ],
        ),
    ]