# Generated by Django 4.2.3 on 2023-07-31 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_alter_section_course_alter_videodocument_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='thumbnails/'),
        ),
    ]
