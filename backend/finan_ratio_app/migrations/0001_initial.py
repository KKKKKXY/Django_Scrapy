# Generated by Django 3.1.5 on 2021-03-21 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RatioYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(blank=True, db_column='company_id', max_length=20, null=True)),
                ('year', models.CharField(blank=True, db_column='year', max_length=20, null=True)),
                ('ratio', models.CharField(blank=True, db_column='ratio', max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Scraped Ratio Year Detail',
                'verbose_name_plural': 'Scraped Ratio Year Details',
                'db_table': 'ratio_year_detail',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PRatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(blank=True, db_column='company_id', max_length=20, null=True)),
                ('gross_profit_mar', models.ManyToManyField(blank=True, db_column='gross_profit_mar', max_length=255, related_name='gross_profit_mar', to='finan_ratio_app.RatioYear')),
                ('net_profit_mar', models.ManyToManyField(blank=True, db_column='net_profit_mar', max_length=255, related_name='net_profit_mar', to='finan_ratio_app.RatioYear')),
                ('opera_inc_on_reve_r', models.ManyToManyField(blank=True, db_column='opera_inc_on_reve_r', max_length=255, related_name='opera_inc_on_reve_r', to='finan_ratio_app.RatioYear')),
                ('ret_on_asset', models.ManyToManyField(blank=True, db_column='ret_on_asset', max_length=255, related_name='ret_on_asset', to='finan_ratio_app.RatioYear')),
                ('ret_on_equity', models.ManyToManyField(blank=True, db_column='ret_on_equity', max_length=255, related_name='ret_on_equity', to='finan_ratio_app.RatioYear')),
            ],
            options={
                'verbose_name': 'Scraped Profit Ratio',
                'verbose_name_plural': 'Scraped Profit Ratios',
                'db_table': 'profit_ratio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='OERatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(blank=True, db_column='company_id', max_length=20, null=True)),
                ('opera_expe_to_t_reve_r', models.ManyToManyField(blank=True, db_column='opera_expe_to_t_reve_r', max_length=255, related_name='opera_expe_to_t_reve_r', to='finan_ratio_app.RatioYear')),
                ('t_asset_tur', models.ManyToManyField(blank=True, db_column='t_asset_tur', max_length=255, related_name='t_asset_tur', to='finan_ratio_app.RatioYear')),
            ],
            options={
                'verbose_name': 'Scraped Operat Effici Ratio',
                'verbose_name_plural': 'Scraped Operat Effici Ratios',
                'db_table': 'operat_effici_ratio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='LRatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(blank=True, db_column='company_id', max_length=20, null=True)),
                ('acco_pay_tur', models.ManyToManyField(blank=True, db_column='acco_pay_tur', max_length=255, related_name='acco_pay_tur', to='finan_ratio_app.RatioYear')),
                ('acco_recei_tur', models.ManyToManyField(blank=True, db_column='acco_recei_tur', max_length=255, related_name='acco_recei_tur', to='finan_ratio_app.RatioYear')),
                ('curr_r', models.ManyToManyField(blank=True, db_column='curr_r', max_length=255, related_name='curr_r', to='finan_ratio_app.RatioYear')),
                ('invent_tur', models.ManyToManyField(blank=True, db_column='invent_tur', max_length=255, related_name='invent_tur', to='finan_ratio_app.RatioYear')),
            ],
            options={
                'verbose_name': 'Scraped Liquid Ratio',
                'verbose_name_plural': 'Scraped Liquid Ratios',
                'db_table': 'liquid_ratio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FPPRatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(blank=True, db_column='company_id', max_length=20, null=True)),
                ('asse_to_equi_r_finan_lev', models.ManyToManyField(blank=True, db_column='asse_to_equi_r_finan_lev', max_length=255, related_name='asse_to_equi_r_finan_lev', to='finan_ratio_app.RatioYear')),
                ('debt_to_asse_r', models.ManyToManyField(blank=True, db_column='debt_to_asse_r', max_length=255, related_name='debt_to_asse_r', to='finan_ratio_app.RatioYear')),
                ('debt_to_capi_r', models.ManyToManyField(blank=True, db_column='debt_to_capi_r', max_length=255, related_name='debt_to_capi_r', to='finan_ratio_app.RatioYear')),
                ('debt_to_equi_r', models.ManyToManyField(blank=True, db_column='debt_to_equi_r', max_length=255, related_name='debt_to_equi_r', to='finan_ratio_app.RatioYear')),
            ],
            options={
                'verbose_name': 'Scraped Finan Posit Propo Ratio',
                'verbose_name_plural': 'Scraped Finan Posit Propo Ratios',
                'db_table': 'finan_posit_propo_ratio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FinancialRatio',
            fields=[
                ('company_id', models.CharField(db_column='company_id', default='Null', max_length=20, primary_key=True, serialize=False, unique=True)),
                ('finan_posit_propo_r', models.ManyToManyField(blank=True, db_column='finan_posit_propo_r', max_length=255, related_name='finan_posit_propo_r', to='finan_ratio_app.FPPRatio')),
                ('liquid_r', models.ManyToManyField(blank=True, db_column='liquid_r', max_length=255, related_name='liquid_r', to='finan_ratio_app.LRatio')),
                ('operat_effici_r', models.ManyToManyField(blank=True, db_column='operat_effici_r', max_length=255, related_name='operat_effici_r', to='finan_ratio_app.OERatio')),
                ('profit_r', models.ManyToManyField(blank=True, db_column='profit_r', max_length=255, related_name='profit_r', to='finan_ratio_app.PRatio')),
            ],
            options={
                'verbose_name': 'Scraped Financial Ratio',
                'verbose_name_plural': 'Scraped Financial Ratios',
                'db_table': 'dbd_finian_ratio',
                'managed': True,
            },
        ),
    ]