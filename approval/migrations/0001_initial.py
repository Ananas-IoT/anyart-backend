# Generated by Django 2.1.3 on 2018-12-01 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CustomLimitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limitation_name', models.CharField(default='', max_length=100)),
                ('authority_name', models.CharField(default='', max_length=100)),
                ('explanation', models.TextField(default='', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserHierarchyWrapper',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('hierarchy_rank', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Veto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('veto_rank', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='approvalgroup',
            name='hierarchy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='approval.Hierarchy'),
        ),
    ]
