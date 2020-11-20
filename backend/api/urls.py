from django.urls import path

from api.acaraAPIs import acara_api
from api.acaraAPIs import test_api
from access_control.dbviews import *
from map import map_api, leaflet_api
from benchmark_report import benchmark_report_api
from powerbi import powerbi_api
from django.views.decorators.csrf import csrf_exempt
from access_control.validation.template_view_jwt_graphql import TokenAuthGraphQLView
from graphene_django.views import GraphQLView
from download import download_api
from api import graphql_view


urlpatterns = [

    #ACARA API endpoints


    #ACARA API for specific school id -->>for dashboard
    # I comment the below endpoints out, since they are no longer used. Fred
    #path('acara/schools/', acara_api.get_acara_schools.as_view(), name='acara_schools'),
    #path('acara/profiles', acara_api.get_acara_profiles.as_view(), name='acara_profiles'),
    #path('acara/<str:acara_id>/profiles', acara_api.get_dashboard_profiles.as_view(), name='dashboard_profiles'),
    #path('acara/<str:acara_id>/locations', acara_api.get_dashboard_locations.as_view(), name='dashboard_locations'),
    #path('acara/<str:acara_id>/finance', acara_api.get_dashboard_finance.as_view(), name='dashboard_finance'),
    #path('acara/<str:acara_id>/grade-enrolments', acara_api.get_dashboard_grade_enrolments.as_view(), name='dashboard_grade_enrolments'),
    #path('acara/<str:acara_id>/destinations', acara_api.get_dashboard_destinations.as_view(), name='dashboard_destinations'),
    #path('acara/<str:acara_id>/outcomes', acara_api.get_dashboard_outcomes.as_view(), name='dashboard_outcomes'),
    #path('acara/<str:acara_id>/naplan', acara_api.get_dashboard_naplan.as_view(), name='dashboard_naplan'),
    #path('acara/<str:acara_id>/attendance', acara_api.get_dashboard_attendance.as_view(), name='dashboard_attendance'),


    #-----------------------------------------------------------------------------------------------------------------------------------
    # graphql endpoints for dashboard, benchmark, and schools
    # Temporarily secured ---- Fred
    #-----------------------------------------------------------------------------------------------------------------------------------
    path(r'graphql', csrf_exempt(graphql_view.graphql_view.as_view(graphiql=True)), name='graphql'),
    path('benchmark', csrf_exempt(graphql_view.graphql_view.as_view(graphiql=True)), name='graphql'),
    path('dashboard', csrf_exempt(graphql_view.graphql_view.as_view(graphiql=True)), name='graphql'),
    path('schools', csrf_exempt(graphql_view.graphql_view.as_view(graphiql=True)), name='graphql'),

    #-----------------------------------------------------------------------------------------------------------------------------------
    #path('test_url', test_api.test_url.as_view(), name='test_url'),

    #-----------------------------------------------------------------------------------------------------------------------------------
    # Access level endpoints
    # Temporarily secured ---- Fred
    #-----------------------------------------------------------------------------------------------------------------------------------
    path('users', csrf_exempt(classbasedviews.users.as_view()), name='users'),
    path('groups', csrf_exempt(classbasedviews.groups.as_view()), name='groups'),
    path('usergroups', csrf_exempt(classbasedviews.usergroups.as_view()), name='usergroups'),
    #path('userPermissions', csrf_exempt(classbasedviews.userPermissions.as_view()), name='userPermissions'),
    path('permissions', csrf_exempt(classbasedviews.permissions.as_view()), name='permissions'),
    path('entities', csrf_exempt(classbasedviews.entities.as_view()), name='entities'),
    path('reports', csrf_exempt(classbasedviews.reports.as_view()), name='reports'),
    #path('admintree', csrf_exempt(classbasedviews.admintree.as_view()), name='admintree'),
    path('admingroup/<str:entity_id>', csrf_exempt(classbasedviews.admingroup.as_view()), name='admingroup'),
    path('adminEntityList', csrf_exempt(classbasedviews.adminEntityList.as_view()), name='adminEntityList'),
    path('adminGroupList', csrf_exempt(classbasedviews.adminGroupList.as_view()), name='adminGroupList'),
    path('adminReportList', csrf_exempt(classbasedviews.adminReportList.as_view()), name='adminReportList'),


    #-----------------------------------------------------------------------------------------------------------------------------------
    #Map endpoints
    #  no permission check is applied - Fred
    #-----------------------------------------------------------------------------------------------------------------------------------
    path('map/categories/<str:ctype>/<int:entity_id>', map_api.getCategories.as_view(), name='getCategories'),
    path('map/filters/<str:ftype>/<int:entity_id>', map_api.getFilters.as_view(), name='getFilters'),
    path('map/terria/<str:layer_type>/<int:entity_id>', csrf_exempt(map_api.terriajs.as_view()), name='terriajs'),
    #Leaflet map selection endpoints
    path('map/geojson/<str:state>/<str:region>', leaflet_api.getGeoJson.as_view(), name='getGeoJson'),
    path('map/marker/<str:state>', leaflet_api.getMarkers.as_view(), name='getMarkers'),

    #-----------------------------------------------------------------------------------------------------------------------------------
    #PowerBI endpoints
    #  should be secured -- Fred
    #-----------------------------------------------------------------------------------------------------------------------------------
    path('pbi/reportEmbedInfo/<str:codename>', csrf_exempt(powerbi_api.reportEmbedInfo.as_view()), name='reportEmbedInfo'),
    path('pbi/reportList/<int:entityId>', csrf_exempt(powerbi_api.reportList.as_view()), name='reportList'),
    path('pbi/reportList/<int:entityId>', csrf_exempt(powerbi_api.reportList.as_view()), name='reportList'),

    #-----------------------------------------------------------------------------------------------------------------------------------
    #downloadable documents --- disable temporarily, Fred
    #-----------------------------------------------------------------------------------------------------------------------------------
    path('download/<int:entityId>/<str:reportName>', csrf_exempt(download_api.downloadDocument.as_view()), name='downloadReport'),

    #-----------------------------------------------------------------------------------------------------------------------------------
    #Benchmark Report
    # Temporarily secured ---- Fred
    #-----------------------------------------------------------------------------------------------------------------------------------
    path('benchmarkReport/filters/<int:entity_id>', csrf_exempt(benchmark_report_api.getFilters.as_view()), name='getFilters'),
    path('benchmarkReport/benchmarkReportData', csrf_exempt(benchmark_report_api.benchmarkReportData.as_view()), name='benchmarkReportData'),

]
