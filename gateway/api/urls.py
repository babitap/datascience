from django.urls import path
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from access_control.validation.template_view_jwt_graphql import TokenAuthGraphQLView
from access_control.validation.template_view_jwt import TemplateView_B2C

import requests, json
import urllib.parse

class Deserialize(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


class demo_view_class( TemplateView_B2C ): 
    """
    API to get all school profiles from wide table
    """

    def requestUrl(self, request):
        path = request.scheme + '://' + settings.DATA_TIER + request.path
        queryString = request.META['QUERY_STRING']
        if queryString is not b'':
            path = path + '?' + queryString
                
        return path

    def requestHeaders(self, request):
        headers = {}
        headers['content-type'] = request.content_type
        headers['Authorization'] = request.META['HTTP_AUTHORIZATION']
        return headers

    def get(self, request, *args, **kwargs):
        try:            
            #print('the old url/request:'+request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING'] )
            #print('the new url:'+self.requestUrl(request))
            r = requests.get(self.requestUrl(request), headers=self.requestHeaders(request))
            #print('return from data tier:')
            return HttpResponse(r.content, content_type='application/json')
        except Exception as e: 
            print('excpetion for in demo_view_class:get()')
            #print(repr(e))
            return JsonResponse(data={'message': repr(e)})
    
    def post(self, request, *args, **kwargs):
        try:
            body = ''
            if request.body is not None and request.body is not b'':
                body = request.body                      
          
            #print('the old url/request:'+request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING'] )
            #print('the new url:'+self.requestUrl(request))
            
            r = requests.post(self.requestUrl(request), data=body, headers=self.requestHeaders(request))
            return HttpResponse(r.content, content_type='application/json')
        except Exception as e: 
            return JsonResponse(data={'message': repr(e)})
    
    def patch(self, request, *args, **kwargs):
        try:
            body = ''
            if request.body is not None and request.body is not b'':
                body = request.body
            
            r = requests.patch(self.requestUrl(request), data=body, headers=self.requestHeaders(request))
            return HttpResponse(r.content, content_type='application/json')
        except Exception as e: 
            return JsonResponse(data={'message': repr(e)})
    
    def delete(self, request, *args, **kwargs):
        try:
            body = ''
            if request.body is not None and request.body is not b'':
                body = request.body
            
            r = requests.delete(self.requestUrl(request), data=body, headers=self.requestHeaders(request))
            return HttpResponse(r.content, content_type='application/json')
        except Exception as e: 
            return JsonResponse(data={'message': repr(e)})

class admin_view(demo_view_class):
    #the decorator
    def view_admin_page(f):
        def wrap(request, *args, **kwargs):
            path = request.scheme + '://' + settings.TENANT_NAME + request.path
            url = request.request.scheme + '://' + settings.DATA_TIER + '/api/userPermissions?username=' + request.request.user.username
            headers = {}
            headers['content-type'] = request.request.content_type
            headers['Authorization'] = request.request.META['HTTP_AUTHORIZATION']
            res = requests.get(url, headers=headers)

            permission = Deserialize(res.content)

            params = urllib.parse.parse_qs(request.request.META['QUERY_STRING'])
            #entityId = params.get('entity_id', 0)
            if permission.isSuperUser is not True:
                return HttpResponseForbidden('Permission Denied', content_type='application/json')

            return f(request, *args, **kwargs)
        return wrap
    
    @view_admin_page
    def get(self, request, *args, **kwargs):
        return super().get(request, args, kwargs)


urlpatterns = [
    #ACARA API endpoints
    path('acara/schools/', demo_view_class.as_view(), name='acara_schools'),
    path('acara/profiles', demo_view_class.as_view(), name='acara_profiles'),

    #ACARA API for specific school id -->>for dashboard
    path('acara/<str:acara_id>/profiles', demo_view_class.as_view(), name='dashboard_profiles'),
    path('acara/<str:acara_id>/locations', demo_view_class.as_view(), name='dashboard_locations'),
    path('acara/<str:acara_id>/finance', demo_view_class.as_view(), name='dashboard_finance'),
    path('acara/<str:acara_id>/grade-enrolments', demo_view_class.as_view(), name='dashboard_grade_enrolments'),
    path('acara/<str:acara_id>/destinations', demo_view_class.as_view(), name='dashboard_destinations'),
    path('acara/<str:acara_id>/outcomes', demo_view_class.as_view(), name='dashboard_outcomes'),
    path('acara/<str:acara_id>/naplan', demo_view_class.as_view(), name='dashboard_naplan'),
    path('acara/<str:acara_id>/attendance', demo_view_class.as_view(), name='dashboard_attendance'),

    path(r'graphql', csrf_exempt(demo_view_class.as_view()), name='graphql'),
    path('benchmark', csrf_exempt(demo_view_class.as_view()), name='benchmark'),
    path('dashboard', csrf_exempt(demo_view_class.as_view()), name='dashboard'),
    path('schools', csrf_exempt(demo_view_class.as_view()), name='schools'),  

    #-----------------------------------------------------------------------------------------------------------------------------------

    path('test_url', demo_view_class.as_view(), name='test_url'),

    #-----------------------------------------------------------------------------------------------------------------------------------

    #Access level endpoints
    path('users', csrf_exempt(demo_view_class.as_view()), name='users'),
    path('groups', csrf_exempt(demo_view_class.as_view()), name='groups'),
    path('usergroups', csrf_exempt(demo_view_class.as_view()), name='usergroups'),
    path('permissions', csrf_exempt(demo_view_class.as_view()), name='permissions'),
    path('entities', csrf_exempt(demo_view_class.as_view()), name='entities'),
    path('reports', csrf_exempt(demo_view_class.as_view()), name='reports'),
    path('admintree', csrf_exempt(demo_view_class.as_view()), name='admintree'),    
    path('admingroup/<str:entity_id>', csrf_exempt(demo_view_class.as_view()), name='admingroup'),
    path('adminEntityList', csrf_exempt(demo_view_class.as_view()), name='adminEntityList'),
    path('adminGroupList', csrf_exempt(demo_view_class.as_view()), name='adminGroupList'),
    path('adminReportList', csrf_exempt(demo_view_class.as_view()), name='adminReportList'),

    #-----------------------------------------------------------------------------------------------------------------------------------

    #Map endpoints
    path('map/categories/<str:ctype>/<int:entity_id>', demo_view_class.as_view(), name='getCategories'),
    path('map/filters/<str:ftype>/<int:entity_id>', demo_view_class.as_view(), name='getFilters'),
    path('map/terria/<str:layer_type>/<int:entity_id>', csrf_exempt(demo_view_class.as_view()), name='terriajs'),

    #Leaflet map selection endpoints
    path('map/geojson/<str:state>/<str:region>', demo_view_class.as_view(), name='getGeoJson'),
    path('map/marker/<str:state>', demo_view_class.as_view(), name='getMarkers'),

    #PowerBI endpoints
    path('pbi/reportEmbedInfo/<str:codename>', csrf_exempt(demo_view_class.as_view()), name='reportEmbedInfo'),
    path('pbi/reportList/<int:entityId>', csrf_exempt(demo_view_class.as_view()), name='reportList')
 
]