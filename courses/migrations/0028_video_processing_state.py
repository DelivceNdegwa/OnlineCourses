# Generated by Django 4.2.3 on 2023-08-29 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0027_alter_coursestudent_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='processing_state',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('complete', 'Complete')], default='pending', max_length=20),
        ),
    ]
