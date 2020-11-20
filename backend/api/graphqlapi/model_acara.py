from django.db import models

class AcaraSchoolMaster(models.Model):

    acara_id = models.IntegerField(db_column='ACARA_ID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    school_name = models.TextField(db_column='School_Name')  # Field name made lowercase.
    suburb = models.CharField(db_column='Suburb', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=50, blank=True, null=True)  # Field name made lowercase.
    postcode = models.IntegerField(db_column='Postcode', blank=True, null=True)  # Field name made lowercase.
    school_sector = models.CharField(db_column='School_Sector', max_length=50, blank=True, null=True)  # Field name made lowercase.
    school_type = models.CharField(db_column='School_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    campus_type = models.CharField(db_column='Campus_Type', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rolled_reporting_description = models.CharField(db_column='Rolled_Reporting_Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    governing_body = models.TextField(db_column='Governing_Body', blank=True, null=True)  # Field name made lowercase.
    year_range = models.CharField(db_column='Year_Range', max_length=50, blank=True, null=True)  # Field name made lowercase.
    geolocation = models.CharField(db_column='Geolocation', max_length=50, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'acara_SchoolMaster'

class AcaraSchoolBasicYearly(models.Model):
    acara_id = models.IntegerField(db_column='ACARA_ID', blank=True, null=False,primary_key=True)  # Field name made lowercase.
    calendar_year = models.IntegerField(db_column='Calendar_Year', blank=True, null=True)  # Field name made lowercase.

    teaching_staff = models.IntegerField(db_column='Teaching_Staff', blank=True, null=True)  # Field name made lowercase.
    full_time_equivalent_teaching_staff = models.FloatField(db_column='Full_Time_Equivalent_Teaching_Staff', blank=True, null=True)  # Field name made lowercase.
    non_teaching_staff = models.IntegerField(db_column='Non_Teaching_Staff', blank=True, null=True)  # Field name made lowercase.
    full_time_equivalent_non_teaching_staff = models.FloatField(db_column='Full_Time_Equivalent_Non_Teaching_Staff', blank=True, null=True)  # Field name made lowercase.
    
    total_enrolments = models.IntegerField(db_column='Total_Enrolments', blank=True, null=True)  # Field name made lowercase.
    girls_enrolments = models.IntegerField(db_column='Girls_Enrolments', blank=True, null=True)  # Field name made lowercase.
    boys_enrolments = models.IntegerField(db_column='Boys_Enrolments', blank=True, null=True)  # Field name made lowercase.
    full_time_equivalent_enrolments = models.FloatField(db_column='Full_Time_Equivalent_Enrolments', blank=True, null=True)  # Field name made lowercase.
    
    indigenous_enrolments_percent = models.IntegerField(db_column='Indigenous_Enrolments_Percent', blank=True, null=True)  # Field name made lowercase.
    language_background_other_than_english_percent = models.IntegerField(db_column='Language_Background_Other_Than_English_Percent', blank=True, null=True)  # Field name made lowercase.
    icsea = models.IntegerField(db_column='ICSEA', blank=True, null=True)  # Field name made lowercase.
    bottom_sea_quarter_percent = models.IntegerField(db_column='Bottom_SEA_Quarter_Percent', blank=True, null=True)  # Field name made lowercase.
    lower_middle_sea_quarter_percent = models.IntegerField(db_column='Lower_Middle_SEA_Quarter_Percent', blank=True, null=True)  # Field name made lowercase.
    upper_middle_sea_quarter_percent = models.IntegerField(db_column='Upper_Middle_SEA_Quarter_Percent', blank=True, null=True)  # Field name made lowercase.
    top_sea_quarter_percent = models.IntegerField(db_column='Top_SEA_Quarter_Percent', blank=True, null=True)  # Field name made lowercase.

    enrolments_per_staff = models.FloatField(db_column='Enrolments_Per_Staff', blank=True, null=True)  # Field name made lowercase.
    enrolments_per_teacher = models.FloatField(db_column='Enrolments_Per_Teacher', blank=True, null=True)  # Field name made lowercase.
    enrolments_per_non_teacher = models.FloatField(db_column='Enrolments_Per_Non_Teacher', blank=True, null=True)  # Field name made lowercase.

    enrolments_per_staff_full_time_equivalent = models.FloatField(db_column='Enrolments_Per_Staff_Full_Time_Equivalent', blank=True, null=True)  # Field name made lowercase.
    enrolments_per_teacher_full_time_equivalent = models.FloatField(db_column='Enrolments_Per_Teacher_Full_Time_Equivalent', blank=True, null=True)  # Field name made lowercase.
    enrolments_per_non_teacher_full_time_equivalent = models.FloatField(db_column='Enrolments_Per_Non_Teacher_Full_Time_Equivalent', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        unique_together = (("acara_id","calendar_year"),)
        managed = False
        db_table = 'original_acara_SchoolProfiles_extended'

class AcaraSchoolGradeEnrolments(models.Model):
    acara_id = models.BigIntegerField(db_column='ACARA_ID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    calendar_year = models.BigIntegerField(primary_key=False, db_column='Calendar_Year')  # Field name made lowercase.
    
    two_years_before_year_1_enrolments = models.FloatField(db_column='Two_years_before_Year_1_Enrolments', blank=True, null=True)  # Field name made lowercase.
    one_year_before_year_1_enrolments = models.FloatField(db_column='One_year_before_Year_1_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_1_enrolments = models.FloatField(db_column='Year_1_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_2_enrolments = models.FloatField(db_column='Year_2_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_3_enrolments = models.FloatField(db_column='Year_3_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_4_enrolments = models.FloatField(db_column='Year_4_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_5_enrolments = models.FloatField(db_column='Year_5_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_6_enrolments = models.FloatField(db_column='Year_6_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_7_enrolments = models.FloatField(db_column='Year_7_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_8_enrolments = models.FloatField(db_column='Year_8_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_9_enrolments = models.FloatField(db_column='Year_9_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_10_enrolments = models.FloatField(db_column='Year_10_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_11_enrolments = models.FloatField(db_column='Year_11_Enrolments', blank=True, null=True)  # Field name made lowercase.
    year_12_enrolments = models.FloatField(db_column='Year_12_Enrolments', blank=True, null=True)  # Field name made lowercase.
    primary_ungraded_enrolments = models.FloatField(db_column='Primary_Ungraded_Enrolments', blank=True, null=True)  # Field name made lowercase.
    secondary_ungraded_enrolments = models.BigIntegerField(db_column='Secondary_Ungraded_Enrolments', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because of name conflict.

    class Meta:
        unique_together = (("acara_id","calendar_year"),)
        managed = False
        db_table = 'original_acara_EnrolmentsByGrade'

class AcaraSchoolFinance(models.Model):
    acara_id = models.BigIntegerField(db_column='ACARA_ID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    calendar_year = models.BigIntegerField(primary_key=False, db_column='Calendar_Year')  # Field name made lowercase.
    
    income_aus_recurrent = models.BigIntegerField(db_column='Income_AUS_Recurrent', blank=True, null=True)  # Field name made lowercase.
    income_state_recurrent = models.BigIntegerField(db_column='Income_State_Recurrent', blank=True, null=True)  # Field name made lowercase.
    income_fees_charges_parent = models.BigIntegerField(db_column='Income_Fees_Charges_Parent', blank=True, null=True)  # Field name made lowercase.
    income_other_private = models.BigIntegerField(db_column='Income_Other_Private', blank=True, null=True)  # Field name made lowercase.
    income_total_gross = models.BigIntegerField(db_column='Income_Total_Gross', blank=True, null=True)  # Field name made lowercase.

    deductions_curr_capital_proj = models.BigIntegerField(db_column='Deductions_Curr_Capital_Proj', blank=True, null=True)  # Field name made lowercase.
    deductions_fut_capital_proj = models.BigIntegerField(db_column='Deductions_Fut_Capital_Proj', blank=True, null=True)  # Field name made lowercase.
    deductions_debt_service = models.BigIntegerField(db_column='Deductions_Debt_Service', blank=True, null=True)  # Field name made lowercase.
    deductions_total = models.BigIntegerField(db_column='Deductions_Total', blank=True, null=True)  # Field name made lowercase.

    income_total_net_recurrent = models.BigIntegerField(db_column='Income_Total_Net_Recurrent', blank=True, null=True)  # Field name made lowercase.

    capital_expend_aus = models.BigIntegerField(db_column='Capital_Expend_AUS', blank=True, null=True)  # Field name made lowercase.
    capital_expend_state = models.BigIntegerField(db_column='Capital_Expend_State', blank=True, null=True)  # Field name made lowercase.
    capital_expend_new_school_loans = models.BigIntegerField(db_column='Capital_Expend_New_School_Loans', blank=True, null=True)  # Field name made lowercase.
    capital_expend_curr_capital_proj = models.BigIntegerField(db_column='Capital_Expend_Curr_Capital_Proj', blank=True, null=True)  # Field name made lowercase.
    capital_expend_other_private = models.BigIntegerField(db_column='Capital_Expend_Other_Private', blank=True, null=True)  # Field name made lowercase.
    capital_expend_total = models.BigIntegerField(db_column='Capital_Expend_Total', blank=True, null=True)  # Field name made lowercase.

    FTE_funded_enrolments = models.FloatField(db_column='FTE_Funded_Enrolments', blank=True, null=True)  # Field name made lowercase.

    income_aus_recurrent_per_student = models.FloatField(db_column='Income_Aus_Recurrent_Per_Student', blank=True, null=True)  # Field name made lowercase.
    income_state_recurrent_per_student = models.FloatField(db_column='Income_State_Recurrent_Per_Student', blank=True, null=True)  # Field name made lowercase.
    income_fees_charges_parent_per_student = models.FloatField(db_column='Income_Fees_Charges_Parent_Per_Student', blank=True, null=True)  # Field name made lowercase.
    income_other_private_per_student = models.FloatField(db_column='Income_Other_Private_Per_Student', blank=True, null=True)  # Field name made lowercase.
    income_total_gross_per_student = models.FloatField(db_column='Income_Total_Gross_Per_Student', blank=True, null=True)  # Field name made lowercase.
    
    deductions_curr_capital_proj_per_student = models.FloatField(db_column='Deductions_Curr_Capital_Proj_Per_Student', blank=True, null=True)  # Field name made lowercase.
    deductions_fut_capital_proj_per_student = models.FloatField(db_column='Deductions_Fut_Capital_Proj_Per_Student', blank=True, null=True)  # Field name made lowercase.
    deductions_debt_service_per_student = models.FloatField(db_column='Deductions_Debt_Service_Per_Student', blank=True, null=True)  # Field name made lowercase.
    deductions_total_per_student = models.FloatField(db_column='Deductions_Total_Per_Student', blank=True, null=True)  # Field name made lowercase.

    income_total_net_recurrent_per_student = models.FloatField(db_column='Income_Total_Net_Recurrent_Per_Student', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        unique_together = (("acara_id","calendar_year"),)
        managed = False
        db_table = 'original_acara_Finance'


class AcaraSchoolLocation(models.Model):
    acara_id = models.BigIntegerField(db_column='ACARA_ID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    calendar_year = models.IntegerField(primary_key=False, db_column='Calendar_Year')  # Field name made lowercase.
    
    latitude = models.FloatField(db_column='Latitude', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='Longitude', blank=True, null=True)  # Field name made lowercase.
    sa1_code = models.IntegerField(db_column='SA1_CODE', blank=True, null=True)  # Field name made lowercase.
    sa2_code = models.IntegerField(db_column='SA2_CODE', blank=True, null=True)  # Field name made lowercase.
    sa2_name = models.CharField(db_column='SA2_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sa3_code = models.IntegerField(db_column='SA3_CODE', blank=True, null=True)  # Field name made lowercase.
    sa3_name = models.CharField(db_column='SA3_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sa4_code = models.IntegerField(db_column='SA4_CODE', blank=True, null=True)  # Field name made lowercase.
    sa4_name = models.CharField(db_column='SA4_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        unique_together = (("acara_id","calendar_year"),)
        managed = False
        db_table = 'original_acara_SchoolLocations'    

class AcaraSchoolSecondaryOutcome(models.Model):
    acara_id = models.BigIntegerField(db_column='ACARA_School_ID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    calendar_year = models.IntegerField(primary_key=False, db_column='Calendar_Year')  # Field name made lowercase.
    
    senior_secondary_certificates_awarded = models.FloatField(db_column='Senior_Secondary_Certificates_Awarded', blank=True, null=True)  # Field name made lowercase.
    completed_senior_secondary_school = models.FloatField(db_column='Completed_Senior_Secondary_School', blank=True, null=True)  # Field name made lowercase.
   
    class Meta:
        unique_together = (("acara_id","calendar_year"),)
        managed = False
        db_table = 'original_acara_SecondaryOutcomes'    


class AcaraSchoolStudentAttendance(models.Model):
    acara_id = models.BigIntegerField(db_column='ACARA_School_ID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    calendar_year = models.IntegerField(primary_key=False, db_column='Calendar_Year')  # Field name made lowercase.
    
    attendance_level = models.FloatField(db_column='Attendance_Level', blank=True, null=True)  # Field name made lowercase.
    attendance_rate = models.BigIntegerField(db_column='Attendance_Rate', blank=True, null=True)  # Field name made lowercase.

    indigenous_attendance_level = models.FloatField(db_column='Indigenous_Attendance_Level', blank=True, null=True)  # Field name made lowercase.
    indigenous_attendance_rate = models.FloatField(db_column='Indigenous_Attendance_Rate', blank=True, null=True)  # Field name made lowercase.
    non_indigenous_attendance_level = models.FloatField(db_column='Non_Indigenous_Attendance_Level', blank=True, null=True)  # Field name made lowercase.
    nonindigenous_attendance_rate = models.FloatField(db_column='NonIndigenous_Attendance_Rate', blank=True, null=True)  # Field name made lowercase.    

    class Meta:
        unique_together = (("acara_id","calendar_year"),)
        managed = False
        db_table = 'original_acara_StudentAttendance'    


class AcaraSchoolPostSchoolDestination(models.Model):        
    acara_id = models.BigIntegerField(db_column='ACARA_ID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    calendar_year = models.IntegerField(primary_key=False, db_column='Calendar_Year')  # Field name made lowercase.

    students_at_university = models.BigIntegerField(db_column='Students_at_University', blank=True, null=True)
    students_at_tafe = models.BigIntegerField(db_column='Students_at_TAFE', blank=True, null=True)
    students_in_employment = models.BigIntegerField(db_column='Students_in_Employment', blank=True, null=True)

    class Meta:
        unique_together = (("acara_id","calendar_year"),)
        managed = False
        db_table = 'original_acara_PostSchoolDestinations'    