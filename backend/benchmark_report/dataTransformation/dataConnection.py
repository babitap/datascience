from django.db import connections
import pandas as pd
import datetime
from django.db.models import Max
import geopy.distance
import numpy as np
from access_control.models import *
import json,os,urllib,itertools
import pandas as pd
from access_control.validation.decorators import custom_permission_required
from access_control.validation.validation import *

def stringifyRange(rng):
    string=['%s' for _ in range(len(rng))]
    string=",".join(string)
    return string

def my_custom_sql(query, params_tuble = ()):

    #Run query
    df=pd.read_sql(
      sql=query,
      con=connections['public_data'],
      params=params_tuble
      )
    return df

# get list of all years for search box
def getAllYears():
    years = my_custom_sql("select distinct calendar_year from original_acara_SchoolProfiles_extended order by calendar_year")
    # get the years
    years_df = pd.DataFrame(list(years.values('calendar_year')))
    return years_df['calendar_year'].values.tolist()

# get all information of a school with acara id
def get_school_information(school_id):

    sql = '''
          select top 1 * from original_acara_SchoolProfiles_extended
          where acara_id = %s
          order by calendar_year desc

          '''
    school = my_custom_sql(sql, (school_id,))
    school = school.fillna('')
    school_infor_json = school.to_dict(orient='records')

    return school_infor_json[0]

# get list of all schools name for search box
def getAllSchoolNames():
    sql = '''
          select acara_id as id, school_name, state, suburb, postcode
          from [dbo].[acara_SchoolMaster]
          '''
    schools_df = my_custom_sql(sql, (school_id,))
    return schools_df.to_dict('records')

# get similar schools by selection options and this will not include selected school
def get_data_of_similar_schools_by(selected_school, selected_state, selected_sector, selected_type, year_level, enrol_num_from, enrol_num_to, previousYear, year, enrolTrend,
                                   geoLocationOption, distanceOption_txt):

    para_list = []
    # select similar schools
    sql = '''select p.calendar_year, p.acara_id as acara_id, p.school_name,
            f.Income_Total_Net_Recurrent_Per_Student,  p.full_time_equivalent_teaching_staff,
            p.full_time_equivalent_non_teaching_staff, p.total_enrolments,
            (case when p.full_time_equivalent_non_teaching_staff =0 or p.full_time_equivalent_non_teaching_staff = null then round(p.total_enrolments/0.9,2)
           else round(p.total_enrolments/p.full_time_equivalent_non_teaching_staff,2) end) as nonteachingStaffRate,
           (case when p.full_time_equivalent_non_teaching_staff =0 or p.full_time_equivalent_teaching_staff = null then round(p.total_enrolments/0.9,2)
           else round(p.total_enrolments/p.full_time_equivalent_teaching_staff,2) end) as teachingStaffRate,
            f.Income_Aus_Recurrent, f.Income_State_Recurrent, f.Income_Fees_Charges_Parent, f.Income_Other_Private, f.Income_Total_Gross,
            f.Income_Fees_Charges_Parent_Per_Student, f.Income_Aus_Recurrent_Per_Student, pd.students_at_university, pd.students_at_tafe, pd.students_in_employment,
            sm.latitude as lat,
            sm.longitude as lon '''
    sql += " from dbo.original_acara_SchoolProfiles_extended p join dbo.acara_SchoolMaster sm on p.acara_id =sm.acara_id left join [dbo].[original_acara_Finance] f on p.calendar_year = f.calendar_year and p.acara_id = f.acara_id "
    sql += " left join dbo.original_acara_PostSchoolDestinations pd on p.calendar_year = pd.calendar_year and p.acara_id = pd.acara_id "

    #for year
    sql += " where p.calendar_year = %s ".format(year)
    para_list = para_list+[year]

    # for state
    if selected_state != []:
      sql += " and p.state in ({}) ".format(stringifyRange(selected_state))
      para_list = para_list+selected_state

    # for selected sector
    if selected_sector != []:
      sql += " and p.school_sector in ({}) ".format(stringifyRange(selected_sector))
      para_list = para_list+selected_sector

    # for selected sector
    if geoLocationOption != []:
      sql += " and p.Geolocation in ({}) ".format(stringifyRange(geoLocationOption))
      para_list = para_list+geoLocationOption

    # for selected sector
    if year_level != []:
      sql += " and p.school_type in ({}) ".format(stringifyRange(year_level))
      para_list = para_list+year_level
      
    # these similar schools should not include the selected schools
    sql += " and p.acara_id != %s "
    para_list = para_list+[selected_school]

    print('enrolmetn start')
    print(enrol_num_from)

    if selected_type == "Both Genders":
      if enrol_num_from != None:
        sql += " and p.total_enrolments >= %s "
        para_list = para_list+[enrol_num_from]
      if enrol_num_to != None:
        sql += " and p.total_enrolments < %s"
        para_list = para_list+[enrol_num_to]
    elif  selected_type == "Only Boys":
      if enrol_num_from != None:
        sql += " and p.boys_enrolments >= %s"
        para_list = para_list+[enrol_num_from]
      if enrol_num_to != None:
        sql += " and p.boys_enrolments < %s"
        para_list = para_list+[enrol_num_to]
    else:
      if enrol_num_from != None:
        sql += " and p.girls_enrolments >= %s"
        para_list = para_list+[enrol_num_from]
      if enrol_num_to != None:
        sql += " and p.girls_enrolments < %s"
        para_list = para_list+[enrol_num_to]

    
    similar_school_df = my_custom_sql(sql, tuple(para_list))
    
    ######################start for checking increase or decrease school inrollment
    sql_de = '''select total_enrolments as prevEnroNum, acara_id as acara_id, calendar_year as previousYear
                from dbo.original_acara_SchoolProfiles_extended s where s.calendar_year = %s '''

    similarSchLastYear = my_custom_sql(sql_de, (previousYear,) )
    similar_school_df = similar_school_df.merge(similarSchLastYear,on=['acara_id'])
    similar_school_df['enroChanged'] = similar_school_df['total_enrolments'] - similar_school_df['prevEnroNum']
    if enrolTrend == 'Increase':
        similar_school_df = similar_school_df[similar_school_df['enroChanged']>0]
    elif enrolTrend == 'Decrease':
        similar_school_df = similar_school_df[similar_school_df['enroChanged']<0]

    ################################starting for filter by distance##############
    if distanceOption_txt != None:
        selected_school_infor = get_data_for_selected_school_by(selected_school,previousYear, year)
        centralPoint = (float(selected_school_infor.loc[0,'lat']), float(selected_school_infor.loc[0,'lon']))
        filteredDistanceDF  = pd.DataFrame(data=None, columns=similar_school_df.columns)
        for index, row in similar_school_df.iterrows():
            coords_1 = (float(row['lat']), float(row['lon']))
            if geopy.distance.vincenty(coords_1, centralPoint).km <= distanceOption_txt:
                filteredDistanceDF = filteredDistanceDF.append(row)
        similar_school_df = filteredDistanceDF
    return similar_school_df

def get_data_for_selected_school_by(selected_school,previousYear, year):
    sql = '''select p.calendar_year, p.acara_id as acara_id, p.school_name,
            f.Income_Total_Net_Recurrent_Per_Student,  p.full_time_equivalent_teaching_staff,
            p.full_time_equivalent_non_teaching_staff, p.total_enrolments,
            (case when p.full_time_equivalent_non_teaching_staff =0 or p.full_time_equivalent_non_teaching_staff = null then round(p.total_enrolments/0.9,2)
           else round(p.total_enrolments/p.full_time_equivalent_non_teaching_staff,2) end) as nonteachingStaffRate,
           (case when p.full_time_equivalent_non_teaching_staff =0 or p.full_time_equivalent_teaching_staff = null then round(p.total_enrolments/0.9,2)
           else round(p.total_enrolments/p.full_time_equivalent_teaching_staff,2) end) as teachingStaffRate,
            f.Income_Aus_Recurrent, f.Income_State_Recurrent, f.Income_Fees_Charges_Parent, f.Income_Other_Private, f.Income_Total_Gross,
            f.Income_Fees_Charges_Parent_Per_Student, f.Income_Aus_Recurrent_Per_Student, pd.students_at_university, pd.students_at_tafe, pd.students_in_employment,
            (select top 1 Latitude from dbo.original_acara_SchoolLocations l where l.ACARA_ID = p.ACARA_ID ) lat,
            (select top 1 Longitude from dbo.original_acara_SchoolLocations l where l.ACARA_ID = p.ACARA_ID ) lon'''
    sql += " from dbo.original_acara_SchoolProfiles_extended p left join [dbo].[original_acara_Finance] f on p.calendar_year = f.calendar_year and p.acara_id = f.acara_id "
    sql += " left join dbo.original_acara_PostSchoolDestinations pd on p.calendar_year = pd.calendar_year and p.acara_id = pd.acara_id "

    sql += " where p.calendar_year = %s "
    sql += " and p.acara_id = %s "
    selected_school_df = my_custom_sql(sql, params_tuble = (year,selected_school))

    ######################start for checking increase or decrease school inrollment
    sql_de = '''select total_enrolments as prevEnroNum, acara_id as acara_id, calendar_year as previousYear
                from dbo.original_acara_SchoolProfiles_extended s where s.calendar_year = %s '''
    sql_de += " and s.acara_id = %s "
    SchLastYear = my_custom_sql(sql_de, params_tuble = (previousYear, selected_school,))

    selected_school_df = selected_school_df.merge(SchLastYear,on=['acara_id'])
    selected_school_df['enroChanged'] = selected_school_df['total_enrolments'] - selected_school_df['prevEnroNum']
    return selected_school_df

def getOveralMarketReviewEnrolNum(stateList, yearLevelList, yearFrom, yearTo, centralPointLat,centralPointLon,distanceOption_txt):
    yearlevel_sql = ''
    for yearLevel in yearLevelList:
        yearlevel_sql+=' isnull(sum({}),0) +'.format(yearLevel)

    yearlevel_sql = yearlevel_sql[:-1]
    sql = '''select school_sector, Calendar_Year, '''+yearlevel_sql+''' as total_enrol
            from dbo.original_acara_SchoolEnrolmentsByGrade g
            '''
    if  (centralPointLat == -1 and centralPointLon == -1 and distanceOption_txt == -1):
        sql += 'where '
    else:
        sql += ''' join (select acara_id, max(Latitude) as Latitude, max(Longitude) as Longitude from dbo.original_acara_SchoolLocations group by acara_id) l on l.acara_id = g.acara_id
                    where round((geography::Point(Latitude, Longitude, 4326).STDistance(geography::Point({}, {}, 4326))) / 1000, 1) < {} and
                '''.format(centralPointLat,centralPointLon,distanceOption_txt)

    sql += "  g.state in ({}) ".format(str(stateList).strip('[]'))
    sql += " and g.Calendar_Year >= {} and g.Calendar_Year <= {}".format(yearFrom, yearTo)
    sql += ' group by school_sector,Calendar_Year;'

    overalEnrol = my_custom_sql(sql)
    return overalEnrol
