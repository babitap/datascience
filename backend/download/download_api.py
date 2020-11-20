from django.http import JsonResponse
from django.http import HttpResponse
from access_control.validation.validation import validate_request
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from access_control.models import *

import json,os,urllib,itertools
import urllib.parse

from django.conf import settings
from azure.storage.blob import BlobClient
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity


class downloadDocument(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):

        self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get the content of the downloadable document in Azure storage
        """
        #1, Extract params from query
        entityId = kwargs.get('entityId', '')
        reportName = kwargs.get('reportName', '')
        
        #2, Ensure required params exist and valid
        if entityId == '':
            print('hello I am here1')
            return JsonResponse(data={'message': 'EntityId is required'})
        elif not( int(entityId) == 48004 ) :
            print('hello I am here2')
            return JsonResponse(data={'message': 'No reports are available'})
        elif reportName == '': 
            print('hello I am here3')
            return JsonResponse(data={'message': 'reportName is required'})
        elif not reportName in ('the Catheral School Monthly Enrolment Report', 'the Catheral School Monthly Finance Report'):   ## hardcode temporarily
            print('hello I am here4')
            return JsonResponse(data={'message': 'No report with the name '+reportName  })
        
        
        #3, setup the environment
        table_storage_client = TableService(
            account_name=settings.STORAGE_ACCOUNT,
            account_key=settings.STORAGE_KEY )
        
        #4, retrieve the all the available finance documents ( before expire date )     
        print('---------------tasks:----------------')   
        tasks = table_storage_client.query_entities(
            settings.DOWNLOAD_TABLE , filter="PartitionKey eq '" + reportName + "'")
        
        print(tasks)
        blob_url_dict = {}
        for task in tasks:
            #if task.SASExpireTime and task.SASExpireTime: 
            print(task.FileName)
            print(task.SASUrl)
            blob_url_dict[task.FileName] = task.SASUrl


        return JsonResponse(data={'blob_url':blob_url_dict})

        """
        # test return file 
        blob = BlobClient(account_url="https://downloadableflatfiles.blob.core.windows.net/",
                        container_name="tcsdownload",
                        blob_name="output_2018_10_Finance Committee Documents template updated.docx",
                        credential="Fjd3rvXsQ6RnxA0U2kbaG2hW+mtcgSx33Q02MH33akNF9TqKrTe85VR2yyn6i47LVdaUEbZaZoyqQWiqnomx1Q==")

        data_stream = blob.download_blob()
        content = data_stream.readall()
        return HttpResponse(content, content_type="application/octet-stream")
        """

        """
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
        """
