from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.db import connections
from access_control.validation.template_view_jwt import TemplateView_B2C

import json,os,time,re
import simplejson  
import pandas as pd
import numpy as np
import urllib.parse

null = None
#--------------------------------------------------------------------
#                                Helpers
#--------------------------------------------------------------------

def frameResponse(df, orient='records', dataset_name='List'):  # ref: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html
 
  #Set response in proper format
  response={'Data':{ dataset_name:[]  }, 'Errors':[]}

  #Get frame
  response['Data'][dataset_name]=df.to_dict( orient=orient )

  # switch to HttpResponse due to invalid NaN value in Json, and simplejson package has smart dumps for NaN - Fred
  return HttpResponse( simplejson.dumps(response,ignore_nan=True) , content_type='application/json')

def stringifyRange(rng):
    string=['%s' for _ in range(len(rng))]
    string=",".join(string)
    return string

def parseQueryParams(s):
    d = {}
    for k,v in urllib.parse.parse_qs(s).items():
        match = re.match(r'(?P<k>[^\[]+)\[(?P<v>[^\]]+)\]', k)
        if match:
            gd = match.groupdict()
            d.setdefault(gd['k'], {})[gd['v']] = v#[0]
        else:
            d[k]={'in':v}
    return d

def getCompareIdentifier(x):
    identifiers = {
        'lte':'<=',
        'lt':'<',
        'eq':'=',
        'gt':'>',
        'gte':'>=',
        'in':'in',
        'like':'like'
        }
    return identifiers[x]

def getValueString(x):
      return x if isinstance(x,str) else '('+stringifyRange(x)+')'

def getUrlSqlMap(x):
    urlSqlMap = {
        'acara_id':'ACARA_ID',
        'state':'State',
        'sector':'School_Sector',
        'type':'School_Type',
        'gender':'School_Gender',
        'size':'Total_Enrolments',
        'remoteness':'ABS_Remoteness_Area',
        'year':'Year',
        'metric':'Metric'
        }
    return urlSqlMap[x]

def setParamsTuple(params):
    #Iterate thru parameter items
    params_string,params_list=[],[]
    for item,operations in params.items():

        #Iterate thru this item's operations
        for k,v in operations.items():
            params_string.append(' '.join([getUrlSqlMap(item), getCompareIdentifier(k), getValueString(v)]))
            params_list += v

    #Output param details 
    return params_string,tuple(params_list)

#--------------------------------------------------------------------
#                                API Endpoints
#--------------------------------------------------------------------

class get_acara_schools( TemplateView_B2C ): 

    """
    API to get all school profiles from wide table
    """

    def get(self, request, **kwargs):
        #SQL
        sql = """
                select TOP 100 ACARA_ID, School_Name, Suburb, State, 
                        Postcode, School_Sector, School_Type, Geolocation 
                        from acara_SchoolMaster
        """
        print(sql)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
        #    params=params
            )

        return frameResponse(df,dataset_name= 'Schools')

class get_acara_school_profile( TemplateView_B2C ):

    """
    API to get all school profiles with filters
    """

    def get(self, request):

        #Convert query string to dictionary
        query_params = parseQueryParams(request.META['QUERY_STRING'])
        print(query_params)

        #Set parameters
        params_sql, params = setParamsTuple(query_params)
        print(params_sql)
        print(params)

        #SQL
        sql = """
            select * from [dbo].[acara_SchoolMaster]
        """
        if len(params_sql)>0: sql += ' where ' + ' and '.join(params_sql)
        print(sql)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df)

class get_acara_profiles( TemplateView_B2C ):

    """
    API to get profiles with skinny table structure with specified filters
    """

    def get(self, request):

        #Convert query string to dictionary
        query_params = parseQueryParams(request.META['QUERY_STRING'])
        print(query_params)

        #Set parameters
        params_sql, params = setParamsTuple(query_params)
        print(params_sql)
        print(params)

        #SQL
        sql = """
            select B.* from [dbo].[acara_SchoolMaster] as A
            join [dbo].[acara_SchoolProfiles] as B on A.ACARA_ID=B.ACARA_ID
        """
        if len(params_sql)>0: 
            #Ensure ambiguity
            params_sql=[s.replace('ACARA_ID','B.ACARA_ID') for s in params_sql]
            sql += ' where ' + ' and '.join(params_sql)
        print(sql)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        #Format output
        df=pd.pivot_table(df, index=['ACARA_ID','Year'], columns='Metric', values='Value').reset_index()
        print(df.head())

        return frameResponse(df,'list')

#--------------------------------------------------------------------
#                           Dashboard API
#--------------------------------------------------------------------

class get_dashboard_profiles( TemplateView_B2C ):

    """
    API to get specified school profile from wide table
    """

    def get(self, request, **kwargs):

        #SQL
        sql = """
            select * from [dbo].[original_acara_SchoolProfiles_extended]
            where ACARA_ID = %s
        """
        print(sql)

        #Set parameters
        params=(self.kwargs['acara_id'],)
        print(params)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df,orient='List')

class get_dashboard_locations( TemplateView_B2C ):

    def get(self, request, **kwargs):

        #SQL
        sql = """
            select * from [dbo].[original_acara_SchoolLocations]
            where ACARA_ID = %s
        """
        print(sql)

        #Set parameters
        params=(self.kwargs['acara_id'],)
        print(params)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df,orient='List')

class get_dashboard_finance( TemplateView_B2C ):

    def get(self, request, **kwargs):

        #SQL
        sql = """
            select * from [dbo].[original_acara_Finance]
            where ACARA_ID = %s
        """
        print(sql)

        #Set parameters
        params=(self.kwargs['acara_id'],)
        print(params)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df,orient='List')

class get_dashboard_grade_enrolments( TemplateView_B2C ):

    def get(self, request, **kwargs):

        #SQL
        sql = """
            select * from [dbo].[original_acara_EnrolmentsByGrade]
            where ACARA_ID = %s
        """
        print(sql)

        #Set parameters
        params=(self.kwargs['acara_id'],)
        print(params)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df,orient='List')

class get_dashboard_destinations( TemplateView_B2C ):

    def get(self, request, **kwargs):

        #SQL
        sql = """
            select * from [dbo].[original_acara_PostSchoolDestinations]
            where ACARA_ID = %s
        """
        print(sql)

        #Set parameters
        params=(self.kwargs['acara_id'],)
        print(params)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df,orient='List')

class get_dashboard_outcomes( TemplateView_B2C ):

    def get(self, request, **kwargs):

        #SQL
        sql = """
            select * from [dbo].[original_acara_SecondaryOutcomes]
            where ACARA_ID = %s
        """
        print(sql)

        #Set parameters
        params=(self.kwargs['acara_id'],)
        print(params)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df,orient='List')

class get_dashboard_naplan( TemplateView_B2C ):

    def get(self, request, **kwargs):

        #SQL
        sql = """
            select * from [dbo].[original_acara_NaplanResults]
            where ACARA_ID = %s
        """
        print(sql)

        #Set parameters
        params=(self.kwargs['acara_id'],)
        print(params)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df,orient='List')

class get_dashboard_attendance( TemplateView_B2C ):

    def get(self, request, **kwargs):

        #SQL
        sql = """
            select * from [dbo].[original_acara_StudentAttendance]
            where ACARA_ID = %s
        """
        print(sql)

        #Set parameters
        params=(self.kwargs['acara_id'],)
        print(params)

        #Run query
        df=pd.read_sql(
            sql=sql,
            con=connections['public_data'],
            params=params
            )

        return frameResponse(df,orient='List')








###############################################################################################

from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

from access_control.validation.decorators import custom_permission_required
from access_control.models import *
from access_control.dbviews.classbasedviews import *
from access_control.dbviews.helpers import *

import pandas as pd

class test_url(UserPassesTestMixin, TemplateView):

    #class test_url( TemplateView_B2C ):
    def test_func(self):

        return True

    #@custom_permission_required("add_group")
    def get(self, request, **kwargs):

        print('HIIIIIII')
        industry_name='Education'

        #Add 5 users
        if(0):
            User.objects.create_user(username = 'user1@email.com')
            User.objects.create_user(username = 'user2@email.com')
            User.objects.create_user(username = 'user3@email.com', created_by_id=2)
            User.objects.create_superuser(username = 'superuser@email.com')
            User.objects.create_findexuser(username = 'findexuser@email.com')
            User.objects.create_findexuser_all(username = 'findexuser_all@email.com')

        if(0):
            #Get acara entities
            acara_file=os.path.join('access_control','data','school-profile-2008-2018.xlsx')
            df_excel=pd.read_excel(acara_file,sheet_name='School Profile',usecols=['ACARA SML ID','School Name'],index_col=False)
            entities=df_excel.drop_duplicates().values
            for entity in entities:
                Entity(
                    entity_name=entity[1],
                    industry_id=entity[0],
                    industry_name=industry_name,
                    is_active=True
                ).save()

        if(0):
            #Add permissions from file
            perm_file=os.path.join('access_control','data','permissions.csv')
            df_perms=pd.read_csv(perm_file,index_col=False)
            for i,row in df_perms.iterrows():
                Permission(
                    name=row['name'],
                    codename=row['codename'],
                    is_findex=row['is_findex'],
                    is_findex_all=row['is_findex_all'],
                    is_accessible=row['is_accessible']
                ).save()


        #Add 10 schools
        entities=[
            [40000,'Corpus Christi Catholic School'],
            [40001,'Fahan School'],
            [40002,'Geneva Christian College'],
            [40003,'Holy Rosary Catholic School'],
            [40004,'Immaculate Heart of Mary Catholic School'],
            [40005,'John Calvin School'],
            [40006,'Larmenier Catholic School'],
            [40007,'Launceston Church Grammar School'],
            [40008,'St James Catholic College'],
            [40009,'Our Lady of Lourdes Catholic School'],
            [40010,'Our Lady of Mercy Catholic School']
        ]
        #Add 3 groups to schools
        groups=[
        'Principal & Admin', 
        'Teachers', 
        'Other Staff'
        ]
        if(0):
            for entity in entities:
                entity_id = getattr(Entity.objects.get(industry_id=entity[0], industry_name=industry_name), 'id')
                print(entity_id)

                for group in groups:
                    EntityGroup(
                        name=group,
                        description='NEW GROUP',
                        entity_id=entity_id
                    ).save()



        if(0):
            #Add users to groups
            users=['user1@email.com','user2@email.com']
            for user in users:

                #Select user & group
                my_user = User.objects.get(username = user)
                my_group = EntityGroup.objects.get(name='Other Staff', entity_id=5)

                #Add to group
                my_user.groups.add(my_group)


                #Add permissions to group
                perms=['add_group','change_group','delete_group','view_group']
                for perm in perms:

                    #Select perm
                    my_perm = Permission.objects.get(codename=perm)

                    #Add perm
                    my_group.permissions.add(my_perm)

        if(1):
            #Check perms
            my_user = User.objects.get(username = 'findexuser@email.com')
            print(my_user)
            print(my_user.get_all_permissions())
            print('>>',my_user.has_perm('delete_group'))

            my_perm = Permission.objects.get(codename='add_group')
            print(my_perm.is_findex)


        response={'FUNC RUN':True}

        return JsonResponse(response)