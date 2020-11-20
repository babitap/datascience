from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.db import connections
import json,os,urllib,itertools
import pandas as pd
from access_control.validation.decorators import custom_permission_required
from access_control.validation.validation import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from access_control.models import *
from benchmark_report.dataTransformation import StudentTrs
from benchmark_report.dataTransformation import academicPerforTrs
from benchmark_report.dataTransformation import dataConnection
from benchmark_report.benchmark_report_metadata import *
from benchmark_report.dataTransformation.charts import Chart

from access_control.validation.validation import validate_request


def checkUserIdHasPermissionAcaraId(user_id, acara_id ): 
    try: 
        requester_profile = User.objects.get(id=user_id)
        if requester_profile.has_special_user_perm():
            return True 
        else: 
            all_permitted_entities = requester_profile.get_entities() 
            has_permission = False 
            for entity in all_permitted_entities:
                if acara_id == entity['industry_id']: 
                    has_permission = True 
            return has_permission 
    except: 
        return False 


class getFilters(validate_request, UserPassesTestMixin, TemplateView): 

  def test_func(self):
    #self.user = User.objects.get(username = 'user1@email.com')
    return self.validate()

  # get unique values of a columns
  def get_unique_value(tableName, colName):
    #Run query
    sql = """
        select distinct """+colName+"""
        from [dbo].["""+tableName+"""]
        order by """+colName+""" desc
    """

    #Run query
    df=pd.read_sql(
      sql=sql,
      con=connections['public_data'],
      params=()
      )

    return df

  # school information
  def get_school_info(entity_id):
    #Run query
    sql = """
        select  top 1 *
        from original_acara_SchoolProfiles_extended
        where acara_id = %s
        order by calendar_year desc
    """

    #Run query
    df=pd.read_sql(
      sql=sql,
      con=connections['public_data'],
      params=(entity_id,)
      )

    return df

# note: this entity_id should be acara_id ... sorry Thao 
  def get(self, request, entity_id, *args, **kwargs):
    """
    Purpose: Get JSON of filters given metric inputs
    """

    #--------------------------------------------------------------------------------
    # Permission check --- Fred 
    #--------------------------------------------------------------------------------
    if not checkUserIdHasPermissionAcaraId( user_id = self.user.id, acara_id = entity_id ):
      return JsonResponse(data={'message':"No permission"})
    #--------------------------------------------------------------------------------

    #Extract params
    params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
    filterOptions ={}
    # get filter options for fields
    for filter in BenchmarkReportMetadata.filterColumnsDict["filters"]:
      if "defaultOptions" not in filter.keys():
        values = getFilters.get_unique_value('original_acara_SchoolProfiles_extended', filter['dbCol'])[filter['dbCol']].tolist()
        valuesList = []
        for value in values:
          valuesList.append({"label": value  ,"value": value})
        filterOptions[filter['fronEndVarOptions']] = valuesList
      else:
        filterOptions[filter['fronEndVarOptions']] = filter['defaultOptions']

    #print("entity id", entity_id)
        
    # get default selected for fields
    filterDefaultValues = {}
    for filter in BenchmarkReportMetadata.filterColumnsDict["filters"]:
      if "defaultOptions" not in filter.keys():
        values = getFilters.get_school_info(entity_id)[filter['dbCol']].tolist()
        valuesList = []
        for value in values:
          valuesList.append({"label": value  ,"value": value})
        if filter['type'] == "multioption":
          filterDefaultValues[filter['fronEndVarSelectedDefault']] = valuesList
        else:
          filterDefaultValues[filter['fronEndVarSelectedDefault']] = valuesList[0]

      else:
        if filter['type'] == "multioption":
          filterDefaultValues[filter['fronEndVarSelectedDefault']] = [filter['defaultOptions'][0]]
        else:
          filterDefaultValues[filter['fronEndVarSelectedDefault']] = filter['defaultOptions'][0]

    return JsonResponse({'acaraBenchmarkQuery':{'filterOptions':filterOptions,'filterDefaultValues':filterDefaultValues}})

class benchmarkReportData(validate_request, UserPassesTestMixin, TemplateView):

  def test_func(self):
        #self.user = User.objects.get(username = 'user1@email.com')
        return self.validate()

  def post(self, request, *args, **kwargs):
    #Parse request params
    input_json = json.loads(request.body)
        
    params = input_json['params']
    selected_school = params['school_id']
    selected_state = params['school_state']
    selected_sector = params['school_sector']
    geoLocationOption = params['school_geolocation']
    selected_type = params['school_gender']
    year_level = params['school_type']
    enrol_num_from = (params['enrolment_start_value'])
    enrol_num_to = (params['enrolment_end_value'])
    enrolTrend = "All Trends"
    year = params['selected_year']
    previousYear = year - 1
    distanceOption_txt = params['distance_km']
    data = dict()

    #--------------------------------------------------------------------------------
    # Permission check --- Fred 
    #--------------------------------------------------------------------------------
    if not checkUserIdHasPermissionAcaraId( user_id = self.user.id, acara_id = selected_school ):
      return JsonResponse(data={'message':"No permission"})
    #--------------------------------------------------------------------------------

    #get similar schools information
    similar_school_df = dataConnection.get_data_of_similar_schools_by(selected_school, selected_state, selected_sector, selected_type, year_level, enrol_num_from, enrol_num_to, previousYear,
                                                                      year, enrolTrend, geoLocationOption, distanceOption_txt)
    # select data of selected school
    selected_school_dict = dataConnection.get_data_for_selected_school_by(selected_school,previousYear,year)

    # get seleted school information after searching
    schl_infor = dataConnection.get_school_information(selected_school)

    # run for each metric in metadata, and create chart component including position bar chart and summary card
    data['school_infor']=schl_infor
    summary_table = []
    for benchmark_section in BenchmarkReportMetadata.acara_benchmark_report_metrics:
      data[benchmark_section['value']] = []
      for metric in benchmark_section['metrics']:
        chart_data, summary = Chart.get_benchmark_position_chart(similar_school_df[['calendar_year','acara_id',metric['field']]],\
                                                                              selected_school_dict[['calendar_year','acara_id',metric['field']]], metric)
        if chart_data != {}:
          data[benchmark_section['value']].append( chart_data)
        if summary != {}:
          summary_table.append(summary)

   
    data['summary_table'] = summary_table

    ### change in student enrolment
    st_similar_df = similar_school_df[['calendar_year','acara_id','total_enrolments','enroChanged','prevEnroNum','previousYear','school_name']]
    st_selected_scho_df = selected_school_dict[['calendar_year','acara_id','total_enrolments','enroChanged','prevEnroNum','previousYear','school_name']]
    change_in_enrol = StudentTrs.get_data_for_change_in_student_enrolment(st_similar_df, st_selected_scho_df)
    if change_in_enrol != {}:
      data['student_enrol_analysis'].append( change_in_enrol)

    ## academic Performance
    # stack bar chart
    ap_similar_df = similar_school_df[['calendar_year','acara_id','students_at_university', 'students_at_tafe', 'students_in_employment']]
    ap_selected_scho_df = selected_school_dict[['calendar_year','acara_id','students_at_university', 'students_at_tafe', 'students_in_employment']]
    postStudestination = academicPerforTrs.getPostStuDestination(ap_similar_df,ap_selected_scho_df)
    if postStudestination != {}:
      data['academicPerformance'].append( postStudestination)

    # get seleted school information after searching
    data['similar_schl_infor'] = {"similarSchNum": similar_school_df.shape[0] +1}
    data['school_infor']=schl_infor

    #print(data)

    return JsonResponse(data)






        

        
