import graphene

import pandas as pd
import numpy as np

from graphene import Schema 
from graphene_django import DjangoObjectType
from api.graphqlapi.model_acara import AcaraSchoolMaster
from api.graphqlapi.model_acara import AcaraSchoolBasicYearly
from api.graphqlapi.model_acara import AcaraSchoolGradeEnrolments
from api.graphqlapi.model_acara import AcaraSchoolFinance
from api.graphqlapi.model_acara import AcaraSchoolLocation
from api.graphqlapi.model_acara import AcaraSchoolSecondaryOutcome
from api.graphqlapi.model_acara import AcaraSchoolStudentAttendance
from api.graphqlapi.model_acara import AcaraSchoolPostSchoolDestination

from django.db.models import Q

from access_control.models import *
from access_control.dbviews.helpers import *

def checkUserNameHasPermissionAcaraSchool(user_name, acara_id ): 
    try: 
        requester_profile = User.objects.get(username=user_name)
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

def get_data_model_from_name_string( name_string ):
    if name_string == "AcaraSchoolMaster":
        return AcaraSchoolMaster
    elif name_string == "AcaraSchoolBasicYearly":
        return AcaraSchoolBasicYearly
    elif name_string == "AcaraSchoolGradeEnrolments":
        return AcaraSchoolGradeEnrolments
    elif name_string == "AcaraSchoolFinance":
        return AcaraSchoolFinance
    elif name_string == "AcaraSchoolLocation":
        return AcaraSchoolLocation
    elif name_string == "AcaraSchoolSecondaryOutcome":
        return AcaraSchoolSecondaryOutcome
    elif name_string == "AcaraSchoolStudentAttendance":
        return AcaraSchoolStudentAttendance
    elif name_string == "AcaraSchoolPostSchoolDestination":
        return AcaraSchoolPostSchoolDestination
    else: 
        return null 

#--------------------------------------------#
# default ACARA database 
#--------------------------------------------#
DEFAULT_ACARA_DATABASE = 'public_data'

class Q_list: 
    def __init__(self):
        self.data = []
    def add_Q(self, item ):
        self.data.append( item ) 
    def get_filter(self):
        if len(self.data)>0:
            filter = None 
            for i in range(0, len(self.data) ): 
                if i == 0: 
                    filter = self.data[0]
                else: 
                    filter = filter & self.data[i]
            return filter 
        else: 
            return None 

    def get_filter_with_or_logic(self):
        if len(self.data)>0:
            filter = None 
            for i in range(0, len(self.data) ): 
                if i == 0: 
                    filter = self.data[0]
                else: 
                    filter = filter | self.data[i]
            return filter 
        else: 
            return None 

class AcaraSchoolMasterType(DjangoObjectType):
    class Meta:
        model = AcaraSchoolMaster

class AcaraSchoolBasicYearlyType( DjangoObjectType ):
    class Meta:
        model = AcaraSchoolBasicYearly

class AcaraSchoolGradeEnrolmentsType( DjangoObjectType ):
    class Meta:
        model = AcaraSchoolGradeEnrolments

class AcaraSchoolFinanceType( DjangoObjectType ):
    class Meta:
        model = AcaraSchoolFinance

class AcaraSchoolLocationType( DjangoObjectType ):
    class Meta:
        model = AcaraSchoolLocation

class AcaraSchoolSecondaryOutcomeType( DjangoObjectType ):
    class Meta:
        model = AcaraSchoolSecondaryOutcome

class AcaraSchoolStudentAttendanceType( DjangoObjectType ):
    class Meta:
        model = AcaraSchoolStudentAttendance

class AcaraSchoolPostSchoolDestinationType( DjangoObjectType ):
    class Meta:
        model = AcaraSchoolPostSchoolDestination