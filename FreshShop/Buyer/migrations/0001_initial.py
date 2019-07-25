# Generated by Django 2.2.1 on 2019-07-25 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户姓名')),
                ('password', models.CharField(max_length=32, verbose_name='用户密码')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='用户电话')),
                ('connect_address', models.TextField(blank=True, max_length=32, null=True, verbose_name='用户地址')),
                ('email', models.EmailField(max_length=32, verbose_name='用户邮箱')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(max_length=32, verbose_name='收件地址')),
                ('recver', models.CharField(max_length=32, verbose_name='收件人名称')),
                ('recver_phone', models.CharField(max_length=32, verbose_name='收件人电话')),
                ('post_number', models.CharField(max_length=32, verbose_name='收件人邮编')),
                ('buyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer', verbose_name='用户id')),
            ],
        ),
    ]
