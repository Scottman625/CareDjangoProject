# Generated by Django 4.0.5 on 2022-06-28 04:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelCore.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=1)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_servant', models.BooleanField(default=False)),
                ('line_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CityArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MarkupItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('info', models.CharField(blank=True, max_length=255, null=True)),
                ('createdate', models.DateTimeField(auto_now=True, null=True)),
                ('case', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modelCore.case')),
            ],
        ),
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Servant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('score', models.FloatField(blank=True, default=0, null=True)),
                ('is_home', models.BooleanField(default=False)),
                ('home_hourly_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('home_halfday_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('home_oneday_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('is_hospital', models.BooleanField(default=False)),
                ('hospital_hourly_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('hospital_halfday_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('hospital_oneday_wage', models.IntegerField(blank=True, default=0, null=True)),
                ('info', models.CharField(blank=True, max_length=255, null=True)),
                ('is_alltime_service', models.BooleanField(default=False)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.RESTRICT, related_name='servant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('info', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserLicenseShipImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.license')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=0, null=True)),
                ('cityarea', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.cityarea')),
                ('servant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.servant')),
            ],
        ),
        migrations.CreateModel(
            name='ServantWeekdayTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.CharField(choices=[('0', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'All')], max_length=1)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('servant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.servant')),
            ],
        ),
        migrations.CreateModel(
            name='ServantSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('languageSkill', models.CharField(max_length=100)),
                ('servant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.servant')),
            ],
        ),
        migrations.CreateModel(
            name='ServantServiceItemShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.servant')),
                ('service_item', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.serviceitem')),
            ],
        ),
        migrations.CreateModel(
            name='ServantMarkupItemPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pricePercent', models.FloatField(blank=True, default=0, null=True)),
                ('markup_item', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.markupitem')),
                ('servant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.servant')),
            ],
        ),
        migrations.CreateModel(
            name='ServantLicenseShipImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=modelCore.models.image_upload_handler)),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelCore.license')),
                ('servant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='modelCore.servant')),
            ],
        ),
        migrations.CreateModel(
            name='Recipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('age', models.IntegerField(blank=True, default=0, null=True)),
                ('weight', models.IntegerField(blank=True, default=0, null=True)),
                ('disease', models.CharField(blank=True, max_length=100, null=True)),
                ('disease_info', models.CharField(blank=True, max_length=255, null=True)),
                ('conditions', models.CharField(blank=True, max_length=255, null=True)),
                ('conditions_info', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='recipient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PayInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PaymentType', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('MerchantID', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoMerchantTradeNo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoTradeDate', models.DateTimeField(null=True)),
                ('OrderInfoTradeNo', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('OrderInfoTradeAmt', models.IntegerField(default=0, null=True)),
                ('OrderInfoPaymentType', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('OrderInfoChargeFee', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('OrderInfoTradeStatus', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('CardInfoAuthCode', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('CardInfoGwsr', models.IntegerField(default=0, null=True)),
                ('CardInfoProcessDate', models.DateTimeField(null=True)),
                ('CardInfoAmount', models.IntegerField(default=0, null=True)),
                ('CardInfoCard6No', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('CardInfoCard4No', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='modelCore.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_score', models.IntegerField(blank=True, default=0, null=True)),
                ('user_is_rated', models.BooleanField(default=False)),
                ('user_content', models.CharField(blank=True, max_length=255, null=True)),
                ('user_review_createdate', models.DateTimeField(blank=True, null=True)),
                ('servant_score', models.IntegerField(blank=True, default=0, null=True)),
                ('servant_is_rated', models.BooleanField(default=False)),
                ('servant_content', models.CharField(blank=True, max_length=255, null=True)),
                ('servant_review_createdate', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='modelCore.orderstate'),
        ),
        migrations.CreateModel(
            name='CaseServiceItemShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.case')),
                ('service_item', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.serviceitem')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='cityarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='modelCore.cityarea'),
        ),
        migrations.AddField(
            model_name='case',
            name='markup_item',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='modelCore.servantmarkupitemprice'),
        ),
        migrations.AddField(
            model_name='case',
            name='recipient',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='modelCore.recipient'),
        ),
        migrations.AddField(
            model_name='case',
            name='servant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.RESTRICT, to='modelCore.servant'),
        ),
    ]
