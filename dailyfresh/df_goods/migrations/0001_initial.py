# Generated by Django 2.0.1 on 2018-01-31 07:31

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gname', models.CharField(max_length=20)),
                ('gpic', models.ImageField(upload_to='')),
                ('gprice', models.DecimalField(decimal_places=2, max_digits=6)),
                ('gclick', models.IntegerField()),
                ('gkucun', models.IntegerField()),
                ('gjianjie', models.CharField(max_length=255)),
                ('gcontent', tinymce.models.HTMLField()),
                ('gunit', models.CharField(max_length=10)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'goodsinfo',
            },
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'goods_type',
            },
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='df_goods.TypeInfo'),
        ),
    ]
