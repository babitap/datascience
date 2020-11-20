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

class getGeoJson(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):
        self.user = User.objects.get(username = 'user1@email.com')
        return True#self.validate()

    def get(self, request, state, region, *args, **kwargs):
        """
        Purpose: Get geoJSON based on state and region inputs
        """

        #Parse request params
        fid='map/geojson/' + region+'_'+state+'_2016_AUST.json'
        with open(fid) as f:
            geojson=json.load(f)

        return JsonResponse(geojson)

class getMarkers(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):
        self.user = User.objects.get(username = 'user1@email.com')
        return True#self.validate()

    def get(self, request, state, *args, **kwargs):
        """
        Purpose: Get markers based on state input
        """

        #Get ACARA data
        sql = """
            select ACARA_ID as Code, School_Name as Name, Latitude, Longitude
            from [dbo].[acara_SchoolMaster]
            where State = %s
        """

        print(sql)

        #Run query
        df=pd.read_sql(
          sql=sql,
          con=connections['public_data'],
          params=(state,)
          )

        return JsonResponse({'data':df.to_dict('records')})