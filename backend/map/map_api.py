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

from map.helpers import *

#--------------------------------------------------------------------
#                             DATA SOURCES
#--------------------------------------------------------------------
#    These classes set generic methods for the data sources. 
#    These methods are used by the selections and terria classes
#--------------------------------------------------------------------
class abs_region_data():

    def setParamTuple(params):
        #Create list of params in proper order
        params_out=[]
        if 'category' in params: 
            params_out.append(params['category'][0])

        if 'subcategory' in params:
            params_out.append(params['subcategory'][0])

        if 'metric' in params:
            for metric in params['metric']:
                params_out.append(metric)

        if 'state' in params:
            for state in params['state']:
                params_out.append(state)

        if 'region' in params:
            params_out.append(params['region'][0])

        if 'gender' in params:
            params_out.append(params['gender'][0])

        if 'thematic' in params:
            params_out.append(params['thematic'][0])

        if 'year' in params:
            params_out.append(params['year'][0])

        #Output tuple 
        return tuple(params_out)

    def categories():

        #---------------------------------------
        #Get ABS categories - dynamic
        sql = """
            select Category, Sub_Category, Metric
            from [dbo].[abs_Metric]
        """
        #Run query
        df=pd.read_sql(
          sql=sql,
          con=connections['public_data']
          )

        #Base categories
        outdict=dict()
        for cat in df['Category'].unique():
            #Set category entry
            outdict[cat]=dict()

            #Loop subcategories
            df1=df[df['Category']==cat]
            for subcat in df1['Sub_Category'].unique():

                #Set subcat to list of all metrics
                outdict[cat][subcat]=list(df1[df1['Sub_Category']==subcat]['Metric'].unique())

        return outdict

    def filters(params):

        #Run query
        sql = """
            select State,Region,Gender,Thematic,Year from (
            select metricID from [dbo].[abs_Metric]
            where Category = %s and Sub_Category = %s
        """
        sql += "and Metric in ("+stringifyRange(params['metric'])+")"
        sql += """
            ) as selected_metric
            join [dbo].[abs_Filter] as filter_table on filter_table.metricID=selected_metric.metricID
        """

        #Run query
        df=pd.read_sql(
          sql=sql,
          con=connections['public_data'],
          params=abs_region_data.setParamTuple(params)
          )
        #print("set param tuple",abs_region_data.setParamTuple(params))

        def get_year_combos(yrs):
            year_combos=[]
            for comb in itertools.combinations(years,2):
                year_combos.append(comb[0]+'-'+comb[1])
            return year_combos

        #Loop
        outdict=dict()
        for st in df['State'].unique():
            outdict[st]=dict()
            df1=df[df['State']==st]

            for rg in df1['Region'].unique():
                outdict[st][rg]=dict()
                df2=df1[df1['Region']==rg]

                for gd in df2['Gender'].unique():
                    outdict[st][rg][gd]=dict()
                    df3=df2[df2['Gender']==gd]

                    for th in df3['Thematic'].unique():
                        years=[str(int(yr)) for yr in df3[df3['Thematic']==th]['Year'].unique()]
                        outdict[st][rg][gd][th]=years

                        #If thematic is No.
                        if th=='#': 
                            #Add option for density for all years
                            outdict[st][rg][gd]['#/sqkm']=years
                        
                            #All year combos
                            #year_combos=get_year_combos(years)

                            #Add option for change
                            outdict[st][rg][gd][th+' Change']=years#year_combos

                            #Add option for change %
                            outdict[st][rg][gd][th+' Change %']=years#year_combos

        #Set labels for selects
        labeldict={
            'dropdown1':'State',
            'dropdown2':'Region',
            'dropdown3':'Gender',
            'dropdown4':'Thematic',
            'dropdown5':'Year'
        }
        #print("outdic",outdict)

        return outdict,labeldict

    def query(params):

        #---------------------------------------
        #Get ABS data
        #print("params for query", params)

        #Set query
        sql = """
            select Code,Year,Label,sum(Value) as Value 
            from (
                select Code, Year, Label, Value from (
            """
        sql += """
                    select filterID,Year from (
                        select metricID from [dbo].[abs_Metric]
                        where Category = %s and Sub_Category = %s
        """
        sql += "and Metric in ("+stringifyRange(params['metric'])+")"
        sql += """
                    ) as selected_metric
                    join [dbo].[abs_Filter] as filter_table on filter_table.metricID=selected_metric.metricID
                    where
        """ 
        sql += "State in ("+stringifyRange(params['state'])+")"
        sql += """
                    and Region = %s and Gender = %s and Thematic = %s and Year <= %s and Year >= %s 
                ) as selected_filter
                join [dbo].[abs_Value] as value_table on value_table.filterID=selected_filter.filterID
            ) as A group by Code,Year,Label
        """
        params_v = abs_region_data.setParamTuple(params)
        # add start year
        params_v = list(params_v)
        params_v.append(params['dropdown6'][0])
        params_v = tuple(params_v)
        #print("query for region", sql)

        #Run query
        df=pd.read_sql(
          sql=sql,
          con=connections['public_data'],
          params=params_v
          )

        return df

class current_student_region_data():

    def categories():

        #---------------------------------------
        #Get current_student categories - hardcoded >> adhoc analysis
        outdict={
            'Internal Data':{
                'Current Students':
                    ['Open Balance','New Join','Active','Churn','Graduate']
                    }
                    }

        return outdict

    def filters(params,entity_id):

        #Set filters
        states = ['na']
        regions = ['SA2','SA3','SA4']
        genders = ['na']
        thematics = ['#']
        years = sorted(pd.read_sql(sql="select distinct FILEYEAR as Year from [dbo].["+str(entity_id)+"]",con=connections['student_profile'])['Year'].values)
        years = [int(yr) for yr in years]

        #Loop
        outdict=dict()
        for st in states:
            outdict[st]=dict()

            for rg in regions:
                outdict[st][rg]=dict()

                for gd in genders:
                    outdict[st][rg][gd]=dict()

                    for th in thematics:
                        outdict[st][rg][gd][th]=years

                        #If thematic is No.
                        if th=='#': 
                            #Add option for density for all years
                            outdict[st][rg][gd]['#/sqkm']=years
                        
                            #All year combos
                            #year_combos=get_year_combos(years)

                            #Add option for change
                            outdict[st][rg][gd][th+' Change']=years#year_combos

                            #Add option for change %
                            outdict[st][rg][gd][th+' Change %']=years#year_combos

        #Set labels for selects
        labeldict={
            'dropdown1':'State',
            'dropdown2':'Region',
            'dropdown3':'Gender',
            'dropdown4':'Thematic',
            'dropdown5':'Year'
        }

        #Set multi flag for selects
        multidict={
            'dropdown1':False,
            'dropdown2':False,
            'dropdown3':False,
            'dropdown4':False,
            'dropdown5':False
        }

        return outdict,labeldict#,multidict

    def query(params,entity_id):

        #Validate inputs
        index,label,_ = convertRegionToTbl(params['region'][0])
        if params['metric'][0] not in ['Open Balance','Active','New Join','Churn','Graduate'] or \
                params['region'][0] not in ['SA2','SA3','SA4']:
            return pd.DataFrame()

        #SQL query["""+params['metric'][0]+"""]
        sql="""
            select Code, Label, Year, sum(["""+params['metric'][0]+"""]*RATIO) as Value
            from (
                select """+index+""" as Code,"""+label+""" as Label,FILEYEAR as Year,[Open Balance],Active,[New Join],Churn,Graduate,RATIO
                from (
                    select SUBURB,POSTCODE,FILEYEAR,[Open Balance],Active,[New Join],Churn,Graduate
                    from (
                        --First get by suburb
                        select SUBURB,POSTCODE,FILEYEAR,sum(OpenBalance) as [Open Balance], sum(OpenBalance)+sum(NewJoin) as Active,sum(NewJoin) as [New Join],sum(Churn) as Churn,sum(Graduate) as Graduate 
                        from [dbo].["""+str(entity_id)+"""]
                        group by SUBURB,POSTCODE,FILEYEAR
                    ) as curr
                    left join dbo.abs_Correspondence_SSC_"""+params['region'][0]+""" as corr 
                    on corr.SSC_NAME_2016=curr.SUBURB
                    where SSC_NAME_2016 is null
                ) as null_code
                join dbo.abs_Correspondence_POA_"""+params['region'][0]+""" as corr on corr.POA_Code_2016=null_code.POSTCODE
                union
                select """+index+""" as Code,"""+label+""" as Label,FILEYEAR as Year,[Open Balance],Active,[New Join],Churn,Graduate,RATIO
                from (
                    --First get by suburb
                    select SUBURB,POSTCODE,FILEYEAR,sum(OpenBalance) as [Open Balance], sum(OpenBalance)+sum(NewJoin) as Active,sum(NewJoin) as [New Join],sum(Churn) as Churn,sum(Graduate) as Graduate 
                    from [dbo].["""+str(entity_id)+"""]
                    group by SUBURB,POSTCODE,FILEYEAR
                ) as curr
                left join dbo.abs_Correspondence_SSC_"""+params['region'][0]+""" as corr 
                on corr.SSC_NAME_2016=curr.SUBURB
                where SSC_NAME_2016 is not null
            ) as A
            where Year <= %s and Year >= %s
            group by Code,Label,Year
        """

        #Run query
        df=pd.read_sql(
          sql=sql,
          con=connections['student_profile'],
          params=(params['year'][0],params['dropdown6'][0])
          )

        return df

class acara_marker_data():

    def setParamTuple(params):
        #Create list of params in proper order
        params_out=[]

        if 'metric' in params:
            params_out.append(params['metric'][0])

        if 'state' in params:
            for state in params['state']:
                params_out.append(state)

        if 'sector' in params:
            for sector in params['sector']:
                params_out.append(sector)

        if 'type' in params:
            for t in params['type']:
                params_out.append(t)

        if 'year' in params:
            params_out.append(str(params['year'][0]))

        #Output tuple 
        return tuple(params_out)

    def getMetrics():
        return [
                "Bottom SEA Quarter (%)",
                "Boys Enrolments",
                "Full Time Equivalent Enrolments",
                "Full Time Equivalent Non-Teaching Staff",
                "Full Time Equivalent Teaching Staff",
                "Girls Enrolments",
                "ICSEA",
                "Indigenous Enrolments (%)",
                "Language Background Other Than English (%)",
                "Lower Middle SEA Quarter (%)",
                "Non-Teaching Staff",
                "Teaching Staff",
                "Top SEA Quarter (%)",
                "Total Enrolments",
                "Upper Middle SEA Quarter (%)"
            ]

    def categories():

        #Takes too long.....
        '''#---------------------------------------
                                #Get ACARA categories
                                sql = """
                                    select  'School' as Category,'School Profile' as Sub_Category, Metric
                                    from [dbo].[acara_SchoolProfiles]
                                """
                        
                                print(sql)
                        
                                #Run query
                                df=pd.read_sql(
                                  sql=sql,
                                  con=connections['public_data']
                                  )
                        
                                print(df)'''

        categories=['School']
        subcategories=['School Profile']
        metrics=acara_marker_data.getMetrics()

        #Base categories
        outdict=dict()
        for cat in categories:
            #Set category entry
            outdict[cat]=dict()

            for subcat in subcategories:
                #Set subcat to list of all metrics
                outdict[cat][subcat]=metrics

        return outdict

    def filters(params):

        #---------------------------------------
        #Get ACARA filters
        states=sorted(pd.read_sql(sql="select distinct State from [dbo].[acara_SchoolMaster]",con=connections['public_data'])['State'].values)
        sectors=sorted(pd.read_sql(sql="select distinct School_Sector as [School Sector] from [dbo].[acara_SchoolMaster]",con=connections['public_data'])['School Sector'].values)
        types=sorted(pd.read_sql(sql="select distinct School_Type as [School Type] from [dbo].[acara_SchoolMaster]",con=connections['public_data'])['School Type'].values)
        years=sorted(pd.read_sql(sql="select distinct Calendar_Year as Year from [dbo].[original_acara_SchoolProfiles_extended]",con=connections['public_data'])['Year'].astype(str).values)

        #Map thematic
        thematic_map={
                "Bottom SEA Quarter (%)":['%'],
                "Boys Enrolments":['#'],
                "Full Time Equivalent Enrolments":['#'],
                "Full Time Equivalent Non-Teaching Staff":['#'],
                "Full Time Equivalent Teaching Staff":['#'],
                "Girls Enrolments":['#'],
                "ICSEA":['#'],
                "Indigenous Enrolments (%)":['%'],
                "Language Background Other Than English (%)":['%'],
                "Lower Middle SEA Quarter (%)":['%'],
                "Non-Teaching Staff":['#'],
                "Teaching Staff":['#'],
                "Top SEA Quarter (%)":['%'],
                "Total Enrolments":['#'],
                "Upper Middle SEA Quarter (%)":['%']
            }
        thematics=thematic_map[params['metric'][0]]

        #Loop
        outdict=dict()
        for st in states:
            outdict[st]=dict()

            for sc in sectors:
                outdict[st][sc]=dict()

                for ty in types:
                    outdict[st][sc][ty]=dict()

                    for th in thematics:
                        outdict[st][sc][ty][th]=years

                        #If thematic is No.
                        if th=='#':
                            #Add option for change
                            outdict[st][sc][ty][th+' Change']=years

                            #Add option for change %
                            outdict[st][sc][ty][th+' Change %']=years

        #Set labels for selects
        labeldict={
            'dropdown1':'State',
            'dropdown2':'School Sector',
            'dropdown3':'School Type',
            'dropdown4':'Thematic',
            'dropdown5':'Year'
        }

        return outdict,labeldict

    def query(params):

        #Ensure selected metric in list
        if params['metric'][0] not in acara_marker_data.getMetrics():
            return pd.DataFrame()

        #---------------------------------------
        #Get ACARA data
        sql = """
            select sp.ACARA_ID as Code, School_Name as Label, Value, sp.Year, Latitude, Longitude
            from [dbo].[acara_SchoolProfiles] as sp
            join [dbo].[acara_SchoolMaster] as sm on sm.ACARA_ID=sp.ACARA_ID
            where
        """ 
        sql += "Metric = %s"
        sql += " and State in ("+stringifyRange(params['state'])+")"
        sql += " and School_Sector in ("+stringifyRange(params['sector'])+")" 
        sql += " and School_Type in ("+stringifyRange(params['type'])+")" 
        sql += """ 
            and sp.Year <= %s and sp.Year >= %s
        """

        params_v = acara_marker_data.setParamTuple(params)
        # add start year
        params_v = list(params_v)
        params_v.append(params['dropdown6'][0])
        params_v = tuple(params_v)
        #print("query for marker", sql)


        #Run query
        df=pd.read_sql(
          sql=sql,
          con=connections['public_data'],
          params=params_v
          )

        #print("df marker", df)

        return df

class acara_item_data():

    def query(params,entity_id):


        #---------------------------------------
        #Get ACARA data
        sql = """
            select ACARA_ID as Code, School_Name as Name, Latitude, Longitude
            from [dbo].[acara_SchoolMaster]
            where ACARA_ID = %s
        """


        #Run query
        df=pd.read_sql(
          sql=sql,
          con=connections['public_data'],
          params=(entity_id,)
          )

        return df

#--------------------------------------------------------------------
#                             SELECTIONS
#--------------------------------------------------------------------
#    These classes get the filter values to fill the UI selections
#
#    The UI is split into 2 parts so the selections are split
#    into two as well
#--------------------------------------------------------------------

class getCategories(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):
        return True#self.validate()

    def check_internal_data_exist( entity_id):
        #---------------------------------------
        #Get ACARA data
        sql = """
            Select *
            from INFORMATION_SCHEMA.TABLES where TABLE_NAME = %s
        """


        #Run query
        df=pd.read_sql(
          sql=sql,
          con=connections['student_profile'],
          params=(str(entity_id),)
          )

        if df.empty:
          return False

        return True



    def get(self, request, ctype, entity_id, *args, **kwargs):
        """
        Purpose: Get JSON of categories
        """

        #Extract params
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])


        #======================================================================================================
        if ctype == 'region':

            #---------------------------------------
            #Get ABS categories - dynamic
            outdict=abs_region_data.categories()
            #print("outdict", outdict)

            #---------------------------------------
            #Get current_student categories
            # only get internal data if the selected school has:
            # since we have only 1 school, this will be temporarily hard coded. later should have a flag in database
            #if entity_id == 48004:
            if getCategories.check_internal_data_exist(entity_id) == True:
              temp=current_student_region_data.categories()
              for k,v in temp.items():
                  outdict[k]=v

        #======================================================================================================
        elif ctype == 'marker':

            #---------------------------------------
            #Get ACARA categories
            outdict=acara_marker_data.categories()

        #Set labels for selects
        labeldict={
            'category':'Category',
            'subcategory':'Sub-Category',
            'metric':'Metric'
        }

        return JsonResponse({'labels':labeldict,'data':outdict})

class getFilters(validate_request, UserPassesTestMixin, TemplateView): 

    def test_func(self):

        self.user = User.objects.get(username = 'user1@email.com')
        return True#self.validate()

    def get(self, request, ftype, entity_id, *args, **kwargs):
        """
        Purpose: Get JSON of filters given metric inputs
        """

        #Extract params
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])

        #======================================================================================================
        #Return empty if entity_id is not valid for user
        #if not validateEntityForUser(self.user,entity_id):
        #    outdict,labeldict={},{}

        #======================================================================================================
        #el
        if ftype == 'region':

            #---------------------------------------
            #Get current_student filters - hardcoded >> adhoc analysis
            if params['subcategory'][0] == 'Current Students':
                outdict,labeldict=current_student_region_data.filters(params,entity_id)

            #---------------------------------------
            #Get ABS filters - dynamic
            else:
                outdict,labeldict=abs_region_data.filters(params)

        #======================================================================================================
        elif ftype == 'marker':

            #---------------------------------------
            #Get ACARA categories
            outdict,labeldict=acara_marker_data.filters(params)

        return JsonResponse({'labels':labeldict,'data':outdict})

#--------------------------------------------------------------------
#                             QUERIES
#--------------------------------------------------------------------
#    This class perform queries for the map data dependent 
#    on the inputs
#--------------------------------------------------------------------

class queryData():

    def queryRegions(params,entity_id):

        #---------------------------------------
        #Get current_student - hardcoded >> adhoc analysis
        if params['subcategory'][0] == 'Current Students':
            df=current_student_region_data.query(params,entity_id)

        #---------------------------------------
        #Get ABS data
        else:
            df=abs_region_data.query(params)

        return df

    def queryMarkers(params):
        
        #---------------------------------------
        #Get ACARA data
        df=acara_marker_data.query(params)

        return df

    def queryItem(params,entity_id):

        #---------------------------------------
        #Get ACARA data
        df=acara_item_data.query(params,entity_id)

        return df

#--------------------------------------------------------------------
#                             TERRIAJS
#--------------------------------------------------------------------
#    This class parses the inputs and returns the catalog to the 
#    frontend to display in the terriajs iframe
#--------------------------------------------------------------------

class terriajs(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):
        self.user = User.objects.get(username = 'user1@email.com')
        return True#self.validate()

    def createTerriaLayer(self, layer_type, data, frmt):
        
        #Set json
        terria_json = {
                "baseMapName": "Australian Topography",
                "homeCamera": frmt['camera'],
                "showSplitter": True,
                "catalog": []
            }

        #======================================================================================================
        if layer_type == 'region':

            #Base region layer
            base_layer={
                "id": frmt['id'], 
                "splitDirection": frmt['splitDirection'],
                "type": "csv",
                'name': frmt['name'],
                'data': data.to_csv(index=False),
                'dateFormat':{
                    "timelineTic": "yyyy",
                    "currentTime": "yyyy"
                },
                'hideSource': True,
                'idColumns':[],
                'isShown': True,
                'isSampled': True,
                'isUserSupplied': False,
                'showWarnings': False,
                "regionTypeDimensionId": frmt['regionTypeDimensionId']+"_code"
            }

            #Format region layer
            frmt_layer = {
                'opacity': frmt['formatSelect']['opacity']['value'],
                'tableStyle': {
                    #-->Variables
                    'dataVariable': 'Value',
                }
            }

            #Colour
            if frmt['formatSelect']['colour']['description']=='Single':
                frmt_layer['tableStyle']['colorMap']=frmt['formatSelect']['colour']['value']

            elif frmt['formatSelect']['colour']['description']=='Colour Map':
                frmt_layer['tableStyle']['colorMap']=frmt['formatSelect']['colour']['value']

            #Scale
            if frmt['formatSelect']['scale']['description']=='Auto':
                frmt_layer['tableStyle']['colorBinMethod']='auto'
                frmt_layer['tableStyle']['colorBins']=frmt['formatSelect']['scale']['value']

            elif frmt['formatSelect']['scale']['description']=='Quantile':
                frmt_layer['tableStyle']['colorBinMethod']='quantile'
                frmt_layer['tableStyle']['colorBins']=frmt['formatSelect']['scale']['value']

            elif frmt['formatSelect']['scale']['description']=='Min/Max':
                frmt_layer['tableStyle']['clampDisplayValue']=True
                frmt_layer['tableStyle']['minDisplayValue']=frmt['formatSelect']['scale']['value'][0]
                frmt_layer['tableStyle']['maxDisplayValue']=frmt['formatSelect']['scale']['value'][1]

            #Combine dicts
            terria_json['catalog'].append({**base_layer, **frmt_layer})


        #======================================================================================================
        elif layer_type == 'marker':

            #Base region layer
            base_layer={
                "id": frmt['id'],
                "type": "csv",
                'name': frmt['name'],
                'data': data.to_csv(index=False),
                'dateFormat':{
                    "timelineTic": "yyyy",
                    "currentTime": "yyyy"
                },
                'hideSource': True,
                'idColumns':[],
                'isShown': True,
                'isSampled': True,
                'isUserSupplied': False,
                'showWarnings': False,
            }

            #Format region layer
            frmt_layer = {
                'tableStyle': {
                    #-->Variables
                    'dataVariable': 'Value',
                    #-->Scale
                    'scale': frmt['formatSelect']['size']['value'],
                    'scaleByValue': True,
                }
            }

            #Colour
            if frmt['formatSelect']['colour']['description']=='Single':
                frmt_layer['tableStyle']['colorMap']=frmt['formatSelect']['colour']['value']

            elif frmt['formatSelect']['colour']['description']=='Colour Map':
                frmt_layer['tableStyle']['colorMap']=frmt['formatSelect']['colour']['value']

            #Scale
            if frmt['formatSelect']['scale']['description']=='Auto':
                frmt_layer['tableStyle']['colorBinMethod']='auto'
                frmt_layer['tableStyle']['colorBins']=frmt['formatSelect']['scale']['value']

            elif frmt['formatSelect']['scale']['description']=='Quantile':
                frmt_layer['tableStyle']['colorBinMethod']='quantile'
                frmt_layer['tableStyle']['colorBins']=frmt['formatSelect']['scale']['value']

            elif frmt['formatSelect']['scale']['description']=='Min/Max':
                frmt_layer['tableStyle']['clampDisplayValue']=True
                frmt_layer['tableStyle']['minDisplayValue']=frmt['formatSelect']['scale']['value'][0]
                frmt_layer['tableStyle']['maxDisplayValue']=frmt['formatSelect']['scale']['value'][1]

            #Combine dicts
            terria_json['catalog'].append({**base_layer, **frmt_layer})

        #======================================================================================================
        elif layer_type == 'item':

            terria_json['catalog'].append({

                "id": frmt['id'],
                "name": data['Name'].iat[0],
                "type": "geojson",
                "data": setCirclePolygon(data['Name'].iat[0], data['Latitude'].iat[0], data['Longitude'].iat[0], 100),
                "isEnabled": True,
                "hideSource": True,
                "style": {
                  "marker-size": "50",
                  "marker-color": "#000000",
                  "marker-symbol": "marker",
                }
            })

        #======================================================================================================
        elif layer_type == 'remove_region':

            terria_json['catalog'].append({

                "id": frmt['id'],
                "splitDirection": frmt['splitDirection'],
                "name": 'temp',
                "type": "csv",
                "data": 'sa2_code,Year,Value\n',
                "isEnabled": False,
                "hideSource": True,
                "tableStyle": {
                    "colorMap": "red-white-hsl(240,50%,50%)",
                    "colorBins": 10,
                },
                "dateFormat": {
                    "timelineTic": "yyyy",
                    "currentTime": "yyyy"
                },
            })

        #======================================================================================================
        elif layer_type == 'remove_marker':

            terria_json['catalog'].append({

                "id": frmt['id'],
                'name': 'temp',
                "type": "csv",
                'data': 'Label,Value,Year,Latitude,Longitude,Code\n',
                "isEnabled": False,
                'hideSource': True,
                "tableStyle": {
                    "colorMap": "red-white-hsl(240,50%,50%)",
                    "colorBins": 10,
                },
                'dateFormat':{
                    "timelineTic": "yyyy",
                    "currentTime": "yyyy"
                },
              })

        return terria_json

    def post(self, request, layer_type, entity_id, *args, **kwargs):
        """
        Purpose: Get JSON of filters given metric inputs
        """

        #Parse request params
        input_json = json.loads(request.body)
        params = input_json['params']
        frmt = input_json['format']

        #modify params based on layer type
        params=modify_params(layer_type,params)



        #======================================================================================================
        #Return empty if entity_id is not valid for user
        #if not validateEntityForUser(self.user,entity_id):
        #    error_json = { "Data": {}, "Errors": [{ "Code":'INVALID USER', "Message":'Data for this entity is not allowed for this user'}] }
        #    return JsonResponse(error_json, safe=False, status=401)

        #======================================================================================================
        #el
        if layer_type == 'region':

            #Check thematic
            params,them_type=checkThematic(params)

            #Query data
            df = queryData.queryRegions(params,entity_id)

            #Calc density
            if them_type=='dty': df = calcDensity(df, params['region'][0])

            #Calc differences
            if df['Year'].min() < df['Year'].max():
                if them_type in ['chg','per']:
                    #Calc changes dependent on thematic
                    df = calcDifferences(df, them_type, included_cols = ['Code', 'Label'])
                    
                    #Filter for ridiculous % change
                    df=calcOutliers(df,alpha=5)#df[df[col+' % Change'].between(-1000,1000,inclusive=True)]
                else:
                    #Do nothing
                    pass
            #If same year, drop year
            elif df['Year'].min() == df['Year'].max():
                df=df.drop('Year',axis=1)

            #Round columns
            df=roundCols(df)

            #Rename code column
            r='aus' if params['region'][0]=='Australia' else params['region'][0].lower()
            df=df.rename({'Code':r+'_code'}, axis=1)


        #======================================================================================================
        elif layer_type == 'marker':

            #Check thematic
            params,them_type=checkThematic(params)

            #Query data
            df = queryData.queryMarkers(params)

            #Ensure selected year exists
            t=df[(df['Value']>0)&(df['Year']==int(params['year'][0]))]
            df=df.merge(t['Code'],on=['Code'])

            #Get differences
            if df['Year'].min() < df['Year'].max():
                if them_type in ['chg','per']:
                    #Calc changes dependent on thematic
                    df = calcDifferences(df, them_type, included_cols = ['Code', 'Label','Latitude', 'Longitude'])
                else:
                    #Do nothing
                    pass
            #If same year, drop year
            elif df['Year'].min() == df['Year'].max():
                df=df.drop('Year',axis=1)
            

            #Round values
            df=roundCols(df)

        #======================================================================================================
        # get school location
        elif layer_type == 'item':

            #Query data
            df = queryData.queryItem(params,entity_id)

        #======================================================================================================
        elif layer_type == 'remove':
            df = None

            #Get layer_type from params
            layer_type+='_'+params['type']

        #Create the terriajs layer from the data inputs
        terria_layer = self.createTerriaLayer(layer_type, df, frmt)

        return JsonResponse(terria_layer)
