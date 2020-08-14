# Generated by Django 3.0.2 on 2020-08-10 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_chapter_fileupload_textblock_ytlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='YTLinka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('yt_link_fk', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.Chapter')),
            ],
        ),
    ]
