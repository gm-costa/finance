# Generated by Django 4.2.3 on 2023-07-03 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0003_rename_categoria_categoria_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='icone',
            field=models.ImageField(upload_to='icones/conta'),
        ),
    ]
