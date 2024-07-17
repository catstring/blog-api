# Generated by Django 4.1.13 on 2024-07-17 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_delete_postview'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=255)),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('last_viewed', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
            options={
                'unique_together': {('post', 'session_id')},
            },
        ),
    ]