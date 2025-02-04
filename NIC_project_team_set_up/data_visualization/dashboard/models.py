# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FinancingOfGrossFiscalDeficit(models.Model):
    country = models.CharField(db_column='Country', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    srcyear = models.CharField(db_column='srcYear', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    gross_fiscal_deficit_gfd = models.IntegerField(db_column='Gross_Fiscal_Deficit_GFD', blank=True, null=True)  # Field name made lowercase.
    internal_financing_of_market_borrowings = models.IntegerField(db_column='Internal_financing_of_market_borrowings', blank=True, null=True)  # Field name made lowercase.
    internal_financing_of_national_social_security_fund_nssf_or_small_savings = models.IntegerField(db_column='Internal_financing_of_National_Social_Security_Fund_NSSF_or_small_savings', blank=True, null=True)  # Field name made lowercase.
    internal_financing_of_state_provident_funds = models.SmallIntegerField(db_column='Internal_financing_of_state_provident_funds', blank=True, null=True)  # Field name made lowercase.
    internal_financing_of_special_deposits = models.SmallIntegerField(db_column='Internal_financing_of_special_deposits', blank=True, null=True)  # Field name made lowercase.
    internal_financing_of_drawdown_of_cash_balances = models.IntegerField(db_column='Internal_financing_of_drawdown_of_cash_balances', blank=True, null=True)  # Field name made lowercase.
    internal_financing_with_financing_from_other_sources = models.IntegerField(db_column='Internal_financing_with_financing_from_other_sources', blank=True, null=True)  # Field name made lowercase.
    external_financing = models.IntegerField(db_column='External_financing', blank=True, null=True)  # Field name made lowercase.
    yearcode = models.SmallIntegerField(db_column='YearCode')  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Financing of Gross Fiscal Deficit'


class Jjm(models.Model):
    states = models.CharField(db_column='States', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    districts = models.CharField(db_column='Districts', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    fy = models.CharField(db_column='FY', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    blocks_with_100_percent_household_tap_connection = models.SmallIntegerField(db_column='Blocks_with_100_Percent_Household_tap_connection', blank=True, null=True)  # Field name made lowercase.
    districts_with_100_percent_household_tap_connection = models.BooleanField(db_column='Districts_with_100_Percent_Household_tap_connection', blank=True, null=True)  # Field name made lowercase.
    household_tap_connection = models.IntegerField(db_column='Household_tap_connection', blank=True, null=True)  # Field name made lowercase.
    number_of_women_trained_for_ftk_testing = models.SmallIntegerField(db_column='Number_of_Women_trained_for_FTK_testing', blank=True, null=True)  # Field name made lowercase.
    total_number_of_households = models.IntegerField(db_column='Total_number_of_households', blank=True, null=True)  # Field name made lowercase.
    villages_with_100_percent_household_tap_connection = models.SmallIntegerField(db_column='Villages_with_100_Percent_Household_tap_connection', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'JJM'


class Pmjdy(models.Model):
    srcstatename = models.CharField(db_column='srcStateName', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    srcdistrictname = models.CharField(db_column='srcDistrictName', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    srcyear = models.SmallIntegerField(db_column='srcYear')  # Field name made lowercase.
    number_of_wards_allotted_in_sub_service_areas_ssas = models.SmallIntegerField(db_column='Number_of_wards_allotted_in_Sub_Service_Areas_SSAs', blank=True, null=True)  # Field name made lowercase.
    number_of_wards_surveyed_in_sub_service_areas_ssas = models.SmallIntegerField(db_column='Number_of_wards_surveyed_in_Sub_Service_Areas_SSAs', blank=True, null=True)  # Field name made lowercase.
    household_coverage = models.FloatField(db_column='Household_Coverage', blank=True, null=True)  # Field name made lowercase.
    yearcode = models.SmallIntegerField(db_column='YearCode')  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PMJDY'


class RuralHealthStatistics(models.Model):
    srcstatename = models.CharField(db_column='srcStateName', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    srcdistrictname = models.CharField(db_column='srcDistrictName', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    functional_sub_centres = models.SmallIntegerField(db_column='Functional_Sub_Centres', blank=True, null=True)  # Field name made lowercase.
    functional_primary_health_centres = models.SmallIntegerField(db_column='Functional_Primary_Health_Centres', blank=True, null=True)  # Field name made lowercase.
    functional_community_health_centres = models.SmallIntegerField(db_column='Functional_Community_Health_Centres', blank=True, null=True)  # Field name made lowercase.
    functional_health_and_wellness_centres_sub_centres = models.SmallIntegerField(db_column='Functional_Health_and_Wellness_Centres_Sub_Centres', blank=True, null=True)  # Field name made lowercase.
    functional_health_and_wellness_centres_primary_health_centres = models.SmallIntegerField(db_column='Functional_Health_and_Wellness_Centres_Primary_Health_Centres', blank=True, null=True)  # Field name made lowercase.
    functional_sub_divisional_hospitals = models.SmallIntegerField(db_column='Functional_Sub_Divisional_Hospitals', blank=True, null=True)  # Field name made lowercase.
    functional_district_hospitals = models.SmallIntegerField(db_column='Functional_District_Hospitals', blank=True, null=True)  # Field name made lowercase.
    srcyear = models.CharField(db_column='srcYear', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.
    yearcode = models.SmallIntegerField(db_column='YearCode')  # Field name made lowercase.
    year = models.CharField(db_column='Year', max_length=50, db_collation='Latin1_General_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Rural Health Statistics'
