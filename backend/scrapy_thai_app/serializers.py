from rest_framework import serializers
from scrapy_thai_app.profile_models import DBDCompany_Thai
from django.contrib.auth.models import User, Group

class CompanyThaiSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBDCompany_Thai
        fields = ('company_id', 'company_name', 'company_type', 'company_status', 'company_objective', 'company_directors', 'company_bussiness_type', 'company_bussiness_type_code', 'company_street', 'company_subdistrict', 'company_district', 'company_province', 'company_address', 'company_tel', 'company_fax', 'company_website', 'company_email', 'company_last_registered_id', 'company_fiscal_year', 'created', 'is_changed')