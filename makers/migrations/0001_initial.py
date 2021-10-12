# Generated by Django 3.2.8 on 2021-10-06 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Language', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'languages',
            },
        ),
        migrations.CreateModel(
            name='Maker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('makername', models.CharField(max_length=40)),
                ('makernickname', models.CharField(max_length=40)),
                ('profile', models.ImageField(upload_to='')),
                ('introduce', models.TextField()),
                ('idcard', models.ImageField(upload_to='')),
                ('bankbook_image', models.ImageField(upload_to='')),
                ('status', models.CharField(max_length=40)),
                ('bank', models.CharField(max_length=45)),
                ('account_number', models.IntegerField()),
                ('account_holder', models.CharField(max_length=45)),
                ('productform', models.CharField(max_length=45)),
                ('category', models.ManyToManyField(to='makers.Category')),
                ('language', models.ManyToManyField(to='makers.Language')),
            ],
            options={
                'db_table': 'makers',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'tours',
            },
        ),
        migrations.CreateModel(
            name='Sns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=45)),
                ('maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makers.maker')),
            ],
            options={
                'db_table': 'sns',
            },
        ),
        migrations.CreateModel(
            name='Maker_tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit_people', models.IntegerField()),
                ('limit_load', models.IntegerField()),
                ('maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makers.maker')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makers.tour')),
            ],
            options={
                'db_table': 'maker_tours',
            },
        ),
        migrations.AddField(
            model_name='maker',
            name='region',
            field=models.ManyToManyField(to='makers.Region'),
        ),
        migrations.AddField(
            model_name='maker',
            name='tour',
            field=models.ManyToManyField(through='makers.Maker_tour', to='makers.Tour'),
        ),
        migrations.AddField(
            model_name='maker',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.CreateModel(
            name='Evidence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=45)),
                ('image', models.ImageField(upload_to='')),
                ('maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='makers.maker')),
            ],
            options={
                'db_table': 'evidences',
            },
        ),
    ]