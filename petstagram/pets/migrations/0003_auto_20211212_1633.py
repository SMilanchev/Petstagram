# Generated by Django 3.1.3 on 2021-12-12 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='image_url',
        ),
        migrations.AddField(
            model_name='pet',
            name='image',
            field=models.ImageField(default='', upload_to='pets'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='pet',
            name='type',
            field=models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('parrot', 'Parrot')], max_length=6),
        ),
    ]
