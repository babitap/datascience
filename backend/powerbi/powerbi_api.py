from django.http import JsonResponse
from django.http import HttpResponse
from access_control.validation.validation import validate_request
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from access_control.models import *
from .helpers  import *

import json,os,urllib,itertools
import urllib.parse


class reportEmbedInfo(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):

        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get powerBI embed information for given codename
        """

        #Extract params from query
        codename = kwargs.get('codename', '')

        ##Ensure required params exist

        if codename == '' :
            return JsonResponse(data={'message':'codename is required'})

        try:
            #Check user permission for the report
            report = Report.objects.get(codename=codename)

            if report is not None:
                if self.user.has_perm(perm=report.permission.codename, entityId=report.entity_id):
                    accesstoken = getaccesstoken()
                    embedinfo = getembedparam(accesstoken, report.workspace_id, report.report_id)
                    errorMsg = embedinfo.get('errorMsg', '')
                else:
                    errorMsg = "No permission to view report"
            else:
                errorMsg = 'Report is not found'

            if errorMsg == '':
                return JsonResponse(embedinfo)
            else:
                return JsonResponse(data={'message': errorMsg})

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})

        except Exception as e:
            return JsonResponse(data={'message':repr(e)})

class reportList(validate_request, UserPassesTestMixin, TemplateView):
    def test_func(self):

        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get list of report information for current request user
        """

        #Extract params from query
        entityId = kwargs.get('entityId', '')

        ##Ensure required params exist

        if entityId == '':
            return JsonResponse(data={'message': 'EntityId is required'})

        try:

            output = {
                'reports': {}
            }
            # Make sure current user has access to the entity
            entities = self.user.get_entities()

            # Check permission for given user
            permissions = self.user.get_all_permissions(entityId=entityId)
            permissionIds = list(map(lambda x: x['id'], permissions))

            matchedEntity = next((e for e in entities if e['id'] == entityId), None)

            if matchedEntity is not None:
                isActiveFiler = Q(is_active=True)
                entityFilter = Q(entity=entityId)
                permissionFilter = Q(permission__in=permissionIds)

                #Find report that satisfy the filter
                reports = list(Report.objects.filter(isActiveFiler & entityFilter & permissionFilter)
                    .select_related('category').values('category__name', 'name', 'codename'))

                for report in reports:
                    reportName = report['category__name']
                    if output['reports'].get(reportName) is None:
                        output['reports'][reportName] = []
                    output['reports'][reportName].append(report)

            return JsonResponse(output)

        except User.DoesNotExist:
            return JsonResponse(data={'message': "User does not exist"})

        except Exception as e:
            return JsonResponse(data={'message': repr(e)})
