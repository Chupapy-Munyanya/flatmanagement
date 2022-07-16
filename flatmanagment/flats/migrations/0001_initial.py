# Generated by Django 4.0.6 on 2022-07-15 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('descr', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='BuildingCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('avatar', models.ImageField(upload_to='media/')),
                ('descr', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DealStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('floor', models.IntegerField()),
                ('owner_id', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performer_id', models.BigIntegerField()),
                ('price', models.BigIntegerField()),
                ('description', models.TextField()),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.servicetype')),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('descr', models.TextField()),
                ('apartment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='flats.apartment')),
            ],
        ),
        migrations.CreateModel(
            name='FlatType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rooms', models.IntegerField()),
                ('square', models.FloatField()),
                ('descr', models.TextField()),
                ('schema', models.ImageField(upload_to='media/')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.house')),
            ],
        ),
        migrations.CreateModel(
            name='Entrance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.house')),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField()),
                ('placement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.placement')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.service')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='flats.dealstatus')),
            ],
        ),
        migrations.AddField(
            model_name='apartment',
            name='builder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='flats.buildingcompany'),
        ),
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('placement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flats.placement')),
                ('entrance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.entrance')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flats.flattype')),
            ],
            bases=('flats.placement',),
        ),
        migrations.CreateModel(
            name='Commercial',
            fields=[
                ('placement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flats.placement')),
                ('square', models.FloatField()),
                ('descr', models.TextField()),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flats.house')),
            ],
            bases=('flats.placement',),
        ),
    ]