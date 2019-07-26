# Generated by Django 2.2.1 on 2019-07-25 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='商品类型名称')),
                ('description', models.TextField(verbose_name='商品类型描述')),
                ('picture', models.ImageField(upload_to='buyer/images')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='goods_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Store.GoodsType', verbose_name='商品类型'),
            preserve_default=False,
        ),
    ]
