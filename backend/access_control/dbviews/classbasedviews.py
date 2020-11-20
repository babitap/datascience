from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.db import connections
from django.db.models import F

import json,os,time,re
import urllib.parse

from access_control.models import *
from access_control.dbviews.helpers import *

from access_control.validation.validation import validate_request
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.forms.models import model_to_dict
import simplejson as json
import uuid


#-------------------------------------------------------------------------#
# common class is used to provide some common functions used in this file
#-------------------------------------------------------------------------#
class common():
    
    def checkSuperUser( self, user_id ): 
        try: 
            requester_profile = User.objects.get(id=user_id)
            if requester_profile.has_superuser_perm() : 
                return True
            else: 
                return False 
        except: 
            return False 

    def checkUserPermission(self, user_id, entity_id, required_perm ): 
        try: 
            requester_profile = User.objects.get(id=user_id)
            if requester_profile.has_perm( perm=required_perm , entityId=entity_id ): 
                return True
            else: 
                return False 
        except: 
            return False 

    def getUsersInEntityGroup(self, entity_group_id=None):
        result = []
        activeFilter = Q(is_active=True)

        user_list = list(EntityGroup.objects.get(id=entity_group_id).user_set.filter(activeFilter).values('id', 'username', 'given_name', 'family_name'))
        for user in user_list:
            email_address = user['username']
            display_name = userFullName(user['given_name'], user['family_name'])
            if(display_name.strip() == ''):
                display_name = email_address

            result.append({
                'value': user['id'],
                'label': display_name,
            })
        return result


    def getAvailableUsersInEntity(self, entity_id):
        result = []

        criterion1 = Q(entities__id=entity_id)
        criterion2 = Q(is_active=True)

        available_user = list(User.objects.filter(criterion1 & criterion2).values('id', 'username', 'given_name', 'family_name'))
        for user in available_user:
            email_address = user['username']
            display_name = userFullName(user['given_name'], user['family_name'])
            if(display_name.strip() == ''):
                display_name = email_address

            result.append({
                'value': user['id'],
                'label': display_name
            })
        return result

    def getPermissionsForEntityGroup(self, entity_group_id):
        result = []
        activeFilter = Q(is_active=True)

        egPermissions = EntityGroup.objects.get(id=entity_group_id).permissions.filter(activeFilter).values()
        for perm in egPermissions:
            result.append({
                'value': perm['codename'] ,
                'label': perm['name'],
            })
        return result
    
    def getAvailablePermissions(self):
        result = []

        criterion1 = Q(is_accessible=True)
        criterion2 = Q(is_active=True)

        permissions = Permission.objects.filter(criterion1 & criterion2)
        for perm in permissions:
            result.append({
                'value': perm.codename,
                'label': perm.name,
            })
        return result
    
    def getEntityGroupsInEntity(self, entity_id):
        criterion1 = Q(entity__id__exact=entity_id)
        criterion2 = Q(is_active=True)
        return list(EntityGroup.objects.filter(criterion1 & criterion2).values('id', 'name', 'description'))
    
    def toReportDict(self, report):
        reportDict = {}

        reportDict['id'] = report.id
        reportDict['name'] = report.name
        reportDict['workspace_id'] = report.workspace_id
        reportDict['report_id'] = report.report_id
        reportDict['permission_id'] = report.permission_id
        reportDict['category_id'] = report.category_id
        reportDict['permission__name'] = report.permission.name
        reportDict['category__name'] = report.category.name
        return reportDict
    

#-------------------------------------------------------------------------#
# Response to the 'user' api 
#-------------------------------------------------------------------------#
class users(validate_request, UserPassesTestMixin, TemplateView):

    post_permission   = 'user_management'

    def test_func(self):

        #self.user = User.objects.get(username = 'user2@email.com')
        return self.validate()
    
    #---------------------------------------------------------------------#
    # Get the requester's information ( no permission required)
    #---------------------------------------------------------------------#
    def get(self, request, *args, **kwargs):
        """
        Purpose: Get data given a user_id

        Permission Consideration, status OK  
              > user A can defintely get his own information
              > user A wants to get user B's information
                  no, not supported
        """

        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,[]):
            return JsonResponse(data={'message':'Error with inputs'})
      
        try:
            result = {
                'entityLookUpList': [],
                'label': concatName(self.user.id),
                'specialPermission': False,
                'specialPermissionList':[],
                'permissionList': {},
                'isSuperUser': False,
                'isFindex': False,
                'isFindexAll': False,
                'lastSelectedEntity': None
            }

            #Get all groups for user
            entities = self.user.get_entities()

            if self.user.is_active:
                #Whether user has special permission
                hasSpecialPermission = self.user.is_findex or self.user.is_findex_all or self.user.is_superuser
                result['specialPermission'] = hasSpecialPermission

                if hasSpecialPermission is True:
                    result['specialPermissionList'] = list(map(lambda x: x['codename'], self.user.get_all_permissions()))
                else:
                    entityPermission = {}
                    for entity in list(map(lambda x: x['id'], entities)):
                        entityPermission[entity] = list(map(lambda x: x['codename'], self.user.get_all_permissions(entity)))
                    result['permissionList'] = entityPermission
                
                #Only consider user has super power when they are active
                result['isSuperUser'] = self.user.is_superuser
                result['isFindex'] = self.user.is_findex
                result['isFindexAll'] = self.user.is_findex_all
                if self.user.last_selected_entity is not None:
                    result['lastSelectedEntity'] = model_to_dict(self.user.last_selected_entity, fields=['id', 'entity_name', 'industry_id', 'industry_name'])

            #Get unique list of industry_id for groups
            if self.user.has_perm('view_all_schools') is True:
                entities = list(Entity.objects.values('id', 'industry_id', 'entity_name', 'industry_name'))

            result['entityLookUpList'] = entities

            return JsonResponse(result)

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    #---------------------------------------------------------------------#
    # Add or invite a new user ( need permission )
    #---------------------------------------------------------------------#
    def post(self, request, *args, **kwargs):
        """
        Purpose: Add user_id to the system 
        Permission Consideration, status WIP
            > user A wants to invite user B as a super user / Findex All user / Findex user 
                option 1 - user A must be a super user  ( relvant to H1 issue )

            > user A wants to invite user B as a new user for entity 1
                option 1 - user A is a super user
                option 2 - user A has the permission 'Invite New User' for the related entity
        Steps: 
            > step 1 - 
        """

        #----------------------------------------------------# 
        # 1, check request type
        #----------------------------------------------------# 
        # Make sure request body is valid
        if request.body is None or request.body is b'':
            return JsonResponse(data={'message':'Post body can not be empty'})
                
        # Parse out all the parameters
        request_data = json.loads(request.body)
        email = request_data.get('email', '')
        entities = request_data.get('entities', [])
        selectedEntity = request_data.get('selectedEntity', 0)
        superUser = request_data.get('superUser', False)
        findexUser = request_data.get('findexUser', False)
        findexAllUser = request_data.get('findexAllUser', False)

        # Email is required regardless whether normal user or special user
        request_type = ''
        if email == '' or not( checkEmailString(email) ):
            request_type = 'ERROR_INVALID_EMAIL'
            return JsonResponse(data={'message':'The given email is invalid'})
        elif superUser or findexUser or findexAllUser: 
            request_type = 'ADD_SPECIAL_USER'
        elif len(entities) > 0 and selectedEntity > 0 and selectedEntity in entities : 
            request_type = 'ADD_NORMAL_USER' 
        else: 
            request_type = 'BAD_REQUEST'
            return JsonResponse(data={'message':'Bad request'})

        #----------------------------------------------------# 
        # 2, check the requsters' has proper permission or not
        #----------------------------------------------------# 
        required_permission = self.post_permission
        targeted_entity     = selectedEntity
        
        requester_profile = User.objects.get(id=self.user.id)
        
        request_status = ''
        if not requester_profile.is_active: 
            request_status = 'NOT_PERMITTED_REQUEST'
        elif request_type == 'ADD_SPECIAL_USER':
            if requester_profile.is_superuser:
                request_status = 'PERMITTED_REQUEST'
            else: 
                request_status = 'NOT_PERMITTED_REQUEST'
        elif request_type == 'ADD_NORMAL_USER':
            #all_permisions = requester_profile.get_all_permissions(entityId=selectedEntity)
            has_valid_permission_or_not = requester_profile.has_perm( perm=required_permission, entityId=targeted_entity )
            if has_valid_permission_or_not:
                request_status = 'PERMITTED_REQUEST'
            else: 
                request_status = 'NOT_PERMITTED_REQUEST'
        else: 
            request_status = 'NOT_PERMITTED_REQUEST'

        if request_status == 'NOT_PERMITTED_REQUEST':
            return JsonResponse(data={'message':'No permission'})

        print('request_type='+request_type)
        print('request_status='+request_status)

        #----------------------------------------------------# 
        # 3, check whether to-be-added user exists or not 
        #----------------------------------------------------# 
        new_user_status = ''
        new_user = getUserByEmail(email)
        if new_user is None:
            new_user_status = 'NEW_USER_NOT_EXISTS'
        else: 
            new_user_status = 'NEW_USER_EXISTS'

        #----------------------------------------------------# 
        # 4.1, if the to-be-added user exists already and is normal user, add the related entity to him
        #----------------------------------------------------# 
        if new_user_status == 'NEW_USER_EXISTS':
            if request_type == 'ADD_NORMAL_USER':
                new_user.entities.add(Entity.objects.get(id=targeted_entity))                
        #----------------------------------------------------# 
        # 4.2, if the user does not exist, add new user entry, 
        #      add the related entity to him and send invitation mail
        #----------------------------------------------------# 
        if new_user_status == 'NEW_USER_NOT_EXISTS':
            try: 
                # 4.2.1, add new user entry 
                if request_type == 'ADD_SPECIAL_USER':
                    if superUser is True:
                        new_user = User.objects.create_superuser(username=email)
                    elif findexAllUser is True:
                        new_user = User.objects.create_findexuser_all(username=email)    
                    else: # must be findexUser 
                        new_user = User.objects.create_findexuser(username=email)
                if request_type == 'ADD_NORMAL_USER':
                    new_user = User.objects.create_user(username=email)
                    # 4.2.2, add related entity if it is normal user
                    new_user.entities.add(Entity.objects.get(id=targeted_entity))

                # 4.2.3, send the invitation mail 
                send_invite(new_user.username)
            except Exception as e: 
                 return JsonResponse(data={'message':repr(e)})

        #----------------------------------------------------# 
        # 4.3, prepare the output 
        #----------------------------------------------------# 
        output = {
            'available_users': common().getAvailableUsersInEntity(selectedEntity), 
            'special_user': True if request_type == 'ADD_SPECIAL_USER' else False
        }
        return JsonResponse(output)


    #---------------------------------------------------------------------#
    # update the information for requester, not only supports last selected entity  ( need permission )
    #---------------------------------------------------------------------#
    def patch(self, request, *args, **kwargs):
        """
        Purpose: Change user detail - currently only accept set user last selected entity
        Permission Consideration, status OK  
              > user A updates its his own last entity
              > user A wants to update user B 's last entity
                  no, not supported

        """

        #Extract params from body
        request_data = json.loads(request.body)

        #Ensure required params exist
        lastSelectedEntity = request_data.get('last_selected_entity', 0)

        ##Ensure required params exist  
        if lastSelectedEntity == 0:
            return JsonResponse(data={'message':'Last selected entity can not be null'})

        #Modify name
        try:
            #Initialize tree
            output={
                'user': {},
                'lastSelectedEntity': {}
            }

            #Update entity group detail
            user = User.objects.get(id=self.user.id)
            user.last_selected_entity_id = lastSelectedEntity
            user.save()

            #Query database and return result
            output['user'] = model_to_dict(user, fields=['given_name', 'family_name'])
            output['lastSelectedEntity'] = model_to_dict(user.last_selected_entity, fields=['id', 'entity_name', 'industry_id', 'industry_name'])
            return JsonResponse(output)

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})
              
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})


    #---------------------------------------------------------------------#
    # delete / deactive one user ( need permission )
    #---------------------------------------------------------------------#
    def delete(self, request, *args, **kwargs):
        """
        Purpose: Change active flag to 0 for user_id in DB

        Permission Consideration, status WIP
            > user A wants to delete/deactive user B
                option 1 - user A must be a super user 
        """

        #----------------------------------------------------# 
        # 1, check request type
        #----------------------------------------------------# 
        #Extract params from query
        params = request.DELETE.dict()

        ##Ensure required params exist
        request_type = ''
        
        if checkRequiredParams(params,['username']):
            request_type = 'BAD_REQUEST'
            return JsonResponse(data={'Error':'Bad request'})
        else: 
            if len(params['username'])>0 and checkEmailString(params['username']) : 
                request_type = 'DELETE_USER'                
            else: 
                request_type = 'ERROR_INVALID_EMAIL'
                return JsonResponse(data={'Error':'Bad request'})

        #----------------------------------------------------# 
        # 2, check the requsters' has proper permission or not
        #----------------------------------------------------# 
        request_status = ''

        requester_profile = User.objects.get(id=self.user.id)
        if not requester_profile.is_active: 
            request_status = 'NOT_PERMITTED_REQUEST'

            if request_type == 'DELETE_USER':
                if requester_profile.is_superuser:
                    request_status = 'PERMITTED_REQUEST'
                else: 
                    request_status = 'NOT_PERMITTED_REQUEST'

        if request_status == 'NOT_PERMITTED_REQUEST':
            return JsonResponse(data={'message':'No permission'})

        #----------------------------------------------------# 
        # 3, deactive user 
        #----------------------------------------------------# 
        #Delete group from DB
        #Delete means to turn active status off
        try:
            #Get user
            user = User.objects.get(username = params['username'])
            user.is_active=False
            user.save()

            return JsonResponse({'message':'User status deactivated'})
            
        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})
              
        except Exception as e:
            return JsonResponse(data={'message':repr(e)})

#-------------------------------------------------------------------------#
# Response to the 'groups' api 
#-------------------------------------------------------------------------#
class groups(validate_request, UserPassesTestMixin, TemplateView):

    get_permission      = 'user_management'
    post_permission     = 'user_management'
    patch_permission    = 'user_management'
    delete_permission   = 'user_management'

    def test_func(self):

        #self.user = User.objects.get(username = 'user2@email.com')
        return self.validate()

    def get(self, request, **kwargs):
        """
        Purpose: Get user groups for the selected entity

        Permission Consideration, status OK  
              > user A can defintely get his own user group
              > user A wants to get user B's information
                  no, not supported

        """

        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['industry_id','industry_name']):
            return JsonResponse(data={'message':'Error with inputs'})

        try:
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = getattr( Entity.objects.get( industry_id = params['industry_id'][0]), 'id' )

            com = common()
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.get_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #Get all groups for entity
            groups = EntityGroup.objects.select_related('entity').filter(entity__industry_id = params['industry_id'][0])
            print(groups)

            #Get unique list of industry_id for groups
            groups_dict = [{'id':g.id, 'name':g.name, 'description':g.description} for g in groups]
            print(groups_dict)

            return JsonResponse({'data':groups_dict})
            
        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"Entity does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def post(self, request, *args, **kwargs):
        """
        Purpose: Add group to entity
        """
        #params = request.POST.dict()
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['entity_id','name','description']):
            return JsonResponse(data={'message':'Error with inputs'})
      
        try:
            com = common()

            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = params['entity_id'][0]

            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.post_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #----------------------------------------------------# 
            # Validate the input
            #----------------------------------------------------# 
            if not checkStringHasOnlyAlphaAndSpace( params['name'][0] ):
                return JsonResponse(data={'message':'Group name only allows alphabet and space'})

            if not checkStringHasOnlyAlphaNumberDashAndSpace( params['description'][0] ):
                return JsonResponse(data={'message':'Group description only allows alphabet, numbers, space and dash'})

             #Initialize tree
            output={
                'groups': []
            }

            #Get entity id
            #entity_id = getattr(Entity.objects.get(industry_id=params['industry_id'], 
            #                        industry_name=params['industry_name']), 'id')
            #entity_id = getattr( Entity.objects.get(id=params['entity_id'][0]), 'id'  )

            #Add group to table
            EntityGroup(
                name=params['name'][0],
                description=params['description'][0],
                entity_id=params['entity_id'][0]
            ).save()

            #Search groups for given entity id
            output['groups'] = com.getEntityGroupsInEntity(params['entity_id'][0])
            return JsonResponse( output )

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def patch(self, request, *args, **kwargs):
        """
        Purpose: Change group details
        """

        #Extract params from query
        #params = request.PATCH.dict()
        #print(params)
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print(params)        

        ##Ensure required params exist  
        if checkRequiredParams(params,['entity_id','entitygroup_id','name','description']):
            return JsonResponse(data={'message':'Error with inputs'})

        #Modify name
        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = params['entity_id'][0]

            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.patch_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            if not checkStringHasOnlyAlphaAndSpace( params['name'][0] ):
                return JsonResponse(data={'message':'Group name only allows alphabet and space'})

            if not checkStringHasOnlyAlphaNumberDashAndSpace( params['description'][0] ):
                return JsonResponse(data={'message':'Group description only allows alphabet, numbers, space and dash'})

            #Initialize tree
            output={
                'groups': []
            }

            #Update entity group detail
            EntityGroup.objects.filter(id=params['entitygroup_id'][0]).update(name=params['name'][0],description=params['description'][0])

            #Query database and return result
            output['groups'] = com.getEntityGroupsInEntity(params['entity_id'][0])
            return JsonResponse(output)

        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"EntityGroup does not exist"})
              
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def delete(self, request, *args, **kwargs):
        """
        Purpose: Remove a group from entity
        """

        #Extract params from query
        #params = request.DELETE.dict()
        #print(params)
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['entity_id', 'entitygroup_id']):
            return JsonResponse(data={'message':'Error with inputs'})
        
        #Update is_active for group in DB
        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = params['entity_id'][0]

            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.delete_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 
            #Initialize tree
            output={
                'groups': []
            }

            #Update entity group detail
            EntityGroup.objects.filter(id=params['entitygroup_id'][0]).update(is_active=0)

            #Query database and return result
            output['groups'] = com.getEntityGroupsInEntity(params['entity_id'][0])
            return JsonResponse(output)   

        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"EntityGroup does not exist"})
              
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

class usergroups(validate_request, UserPassesTestMixin, TemplateView):

    get_permission      = 'user_management'
    post_permission     = 'user_management'
    patch_permission    = 'user_management'
    delete_permission   = 'user_management'

    def test_func(self):

        #self.user = User.objects.get(username = 'user2@email.com')
        return self.validate()

    def get(self, request, **kwargs):
        """
        Purpose: Get users for the group
        """

        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['entitygroup_id']):
            return JsonResponse(data={'Error':'Error with inputs'})

        try:
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            com = common()
            entity_id = getattr( EntityGroup.objects.get( id = params['entitygroup_id'][0] ) , 'entity' )

            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.get_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #Get users
            users = EntityGroup.objects.get(id=params['entitygroup_id'][0]).user_set.all()

            users_list=list(users.values_list('username', flat=True))
            print(users_list)

            return JsonResponse({'data':users_list})

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})

        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"Group does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})
    
    def post(self, request, *args, **kwargs):
        """
        Purpose: Add user to group
        """

        #Extract params from query
        #params = request.POST.dict()

        
        #print( params )
        #print( request.META['QUERY_STRING'] )
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print( 'in usergroup.post()')
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['industry_id', 'entity_id','entitygroup_id','username']):
            return JsonResponse(data={'message':'Error with inputs'})
      
        try:
            com = common()

            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = getattr( EntityGroup.objects.get( id = params['entitygroup_id'][0] ) , 'entity' )
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.post_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #Initialize output
            output={
                'selected_users':[]
            }

            #Get user
            user = User.objects.get(id = params['username'][0])

            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # some validation might be required to check whether user is eligible to add or not

            #Get group
            group = EntityGroup.objects.get(id = params['entitygroup_id'][0])

            #Add user to group
            user.groups.add(group)

            #Query database again and return result
            output['selected_users'] = com.getUsersInEntityGroup(params['entitygroup_id'][0])
            return JsonResponse(output)

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})

        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"Group does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def delete(self, request, *args, **kwargs):
        """
        Purpose: Removea user from group
        """

        #Extract params from query
        #params = request.DELETE.dict()
        #print(params)
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print( 'in usergroup.delete()'  )
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['industry_id', 'entity_id','entitygroup_id','username']):
            return JsonResponse(data={'message':'Error with inputs'})
    
        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = getattr( EntityGroup.objects.get( id = params['entitygroup_id'][0] ) , 'entity' )
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.delete_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 
            #Initialize output
            output={
                'selected_users':[]
            }

            #Get user
            user = User.objects.get(id = params['username'][0])

            #Get group
            group = EntityGroup.objects.get(id = params['entitygroup_id'][0])

            #Remove user to group
            user.groups.remove(group)

            #Query database again and return result
            output['selected_users'] = com.getUsersInEntityGroup(params['entitygroup_id'][0])
            return JsonResponse(output)

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})

        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"Group does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

class permissions(validate_request, UserPassesTestMixin, TemplateView):

    get_permission      = 'user_management'
    post_permission     = 'user_management'
    patch_permission    = 'user_management'
    delete_permission   = 'user_management'

    def test_func(self):

        #self.user = User.objects.get(username = 'user2@email.com')
        return self.validate()

    def get(self, request, **kwargs):
        """
        Purpose: Get permissions for the group
        """

        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['entitygroup_id']):
            return JsonResponse(data={'Error':'Error with inputs'})

        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = getattr( EntityGroup.objects.get( id = params['entitygroup_id'][0] ) , 'entity' )
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.get_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #Get group
            group = EntityGroup.objects.get(id=params['entitygroup_id'][0])

            #List permissions
            perms=list(group.permissions.values_list('codename', flat=True))

            return JsonResponse({'permissions':perms})

        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"Group does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})
    
    def post(self, request, *args, **kwargs):
        """
        Purpose: Add permission to group
        """

        #Extract params from query
        #params = request.POST.dict()
        #print(params)
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print( 'in permissions.post()'  )
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['entitygroup_id','permission_id']):
            return JsonResponse(data={'message':'Error with inputs'})
      
        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = getattr( EntityGroup.objects.get( id = params['entitygroup_id'][0] ) , 'entity' )
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.post_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 
            #Initialize output
            output={
                'selected_permissions':[]
            }

            #Get user
            group = EntityGroup.objects.get(id = params['entitygroup_id'][0])

            #Select perm
            perm = Permission.objects.get(codename=params['permission_id'][0])

            #Add perm
            group.permissions.add(perm)

            #Query database again and return result
            output['selected_permissions'] = com.getPermissionsForEntityGroup(params['entitygroup_id'][0])
            return JsonResponse(output)

        except Permission.DoesNotExist:
            return JsonResponse(data={'message':"Permission does not exist"})

        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"Group does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def delete(self, request, *args, **kwargs):
        """
        Purpose: Remove a permission from group
        """

        #Extract params from query
        #params = request.DELETE.dict()
        #print(params)
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print( 'in permissions.post()'  )
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['entitygroup_id','permission_id']):
            return JsonResponse(data={'message':'Error with inputs'})
      
        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = getattr( EntityGroup.objects.get( id = params['entitygroup_id'][0] ) , 'entity' )
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.delete_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 
            #Initialize output
            output={
                'selected_permissions':[]
            }

            #Get user
            group = EntityGroup.objects.get(id = params['entitygroup_id'][0])

            #Select perm
            perm = Permission.objects.get(codename=params['permission_id'][0])

            #Add perm
            group.permissions.remove(perm)

            #Query database again and return result
            output['selected_permissions'] = com.getPermissionsForEntityGroup(params['entitygroup_id'][0])
            return JsonResponse(output)

        except Permission.DoesNotExist:
            return JsonResponse(data={'message':"Permission does not exist"})

        except EntityGroup.DoesNotExist:
            return JsonResponse(data={'message':"Group does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

class admingroup(validate_request, UserPassesTestMixin, TemplateView):

    get_permission      = 'user_management'

    def test_func(self):

        #self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, entity_id, *args, **kwargs):
        """
        Purpose: Get data given a user_id
        """

        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])
        print(params)

        ##Ensure required params exist
        if checkRequiredParams(params,['group_id']):
            return JsonResponse(data={'message':'Error with inputs'})
      
        try:
            #Init common class
            com = common()

            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.get_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #Initialize output
            output={
                'profile':{},
                'selected_users':[],
                'available_users':[],
                'selected_permissions':[],
                'available_permissions':[]
            }

            #Get entitygroup for inputs
            entitygroup = EntityGroup.objects.get(entity_id = entity_id, id=params['group_id'][0])

            #Get group profile details
            output['profile']={
                'value':entitygroup.id,
                'label':entitygroup.name,
                'description':entitygroup.description,
            }

            #Get users in group
            output['selected_users'] = com.getUsersInEntityGroup(entitygroup.id)

            #Get available users
            output['available_users'] = com.getAvailableUsersInEntity(entitygroup.entity_id)

            #Get permissions for group
            output['selected_permissions'] = com.getPermissionsForEntityGroup(entitygroup.id)

            #Get accessible permissions
            output['available_permissions'] = com.getAvailablePermissions()
            
            return JsonResponse(output)

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})


class adminEntityList(validate_request, UserPassesTestMixin, TemplateView):

    get_permission      = 'user_management'
    def test_func(self):

        #self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get entity list for request user
        """
        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])

        ##Ensure required params exist
        if checkRequiredParams(params,['entity_id']):
            return JsonResponse(data={'message':'Entity id is required'})

        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = params['entity_id'][0]
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.get_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 
                        
            #Initialize tree
            output={
                'value':'education',
                'label':'Education',
                'entities': []
            }
            
            #Entities for user based on groups
            activeFilter = Q(is_active=True)
            entityFilter = Q(id=entity_id)

            # we change the logic here : we only return back the selected entity information... --- Fred 
            if self.user.has_perm('view_all_schools') is False:
                output['entities'] = list(self.user.entities.filter(activeFilter & entityFilter).values('id', name=F('entity_name') ))
            else:
                output['entities'] = list(Entity.objects.filter(activeFilter & entityFilter).values('id', name=F('entity_name') ))

            # make sure that 

            print(output)
            return JsonResponse( output )

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})


class adminGroupList(validate_request, UserPassesTestMixin, TemplateView):

    get_permission      = 'user_management'

    def test_func(self):

        #self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get group list for given enity id
        """

        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])

        ##Ensure required params exist
        if checkRequiredParams(params,['entity_id']):
            return JsonResponse(data={'message':'Entity id is required'})

        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            entity_id = params['entity_id'][0]
            if not com.checkUserPermission( user_id = self.user.id, entity_id = entity_id, required_perm = self.get_permission ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 
            #Initialize tree
            output={
                'groups': []
            }

            #Search groups for given entity id
            output['groups'] = com.getEntityGroupsInEntity(params['entity_id'][0])
            return JsonResponse( output )

        except User.DoesNotExist:
            return JsonResponse(data={'message':"User does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

class adminReportList(validate_request, UserPassesTestMixin, TemplateView):
    #--------------------------------------------------------------#
    # The requester need be a superuser 
    #--------------------------------------------------------------#

    def test_func(self):

        #self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get report list for given enity id, need be a super user 
        """

        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])

        ##Ensure required params exist
        if checkRequiredParams(params,['entity_id']):
            return JsonResponse(data={'message':'Entity id is required'})

        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            if not com.checkSuperUser( user_id = self.user.id ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 
            #Initialize tree
            output={
                'reports': [],
                'permissions':[],
                'reportCategories':[]
            }

            #Only return actual report details for super-user
            if self.user.is_superuser is True:
                output['reports'] = list(Report.objects.filter(Q(entity_id=params['entity_id'][0]) & Q(is_active=1)).values('id', 'name', 'workspace_id', 'report_id', 'permission_id', 'category_id', 'permission__name', 'category__name'))
                output['permissions'] = list(Permission.objects.filter(is_active=1).values('id', 'name'))
                output['reportCategories'] = list(ReportCategory.objects.values('id', 'name'))

            return JsonResponse( output )
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

class userPermissions(validate_request, UserPassesTestMixin, TemplateView):
    #------------------------------------------------------------#
    #  No longer used 
    #------------------------------------------------------------#
    def test_func(self):

        #self.user = User.objects.get(username = 'fred.gu@findex.com.au')
        return self.validate()

    def get(self, request, *args, **kwargs):
        """
        Purpose: Get permissions for given username
        """

        #Extract params from query
        params = urllib.parse.parse_qs(request.META['QUERY_STRING'])

        ##Ensure required params exist
        if checkRequiredParams(params,['username']):
            return JsonResponse(data={'message':'username is required'})

        try:
            com = common()

            #Initialize tree
            output={
                'specialPermission': False,
                'specialPermissionList':[],
                'permissionList': [],
                'isSuperUser': False
            }

            user = User.objects.get(username=params['username'][0])

            #Get all groups for user

            entities = user.get_entities()

            if user.is_active:
                #Whether user has special permission
                hasSpecialPermission = user.is_findex or user.is_findex_all or user.is_superuser
                output['specialPermission'] = hasSpecialPermission

                if hasSpecialPermission is True:
                    output['specialPermissionList'] = list(map(lambda x: x['codename'], self.user.get_all_permissions()))
                else:
                    entityPermission = {}
                    for entity in list(map(lambda x: x['id'], entities)):
                        entityPermission[entity] = list(map(lambda x: x['codename'], self.user.get_all_permissions(entity)))
                    output['permissionList'] = entityPermission
                
                #Only consider user has super power when they are active
                output['isSuperUser'] = user.is_superuser

            return JsonResponse( output )
        
        except User.DoesNotExist:
            return JsonResponse(data={'message':"Permission does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

class entities(validate_request, UserPassesTestMixin, TemplateView):
    #--------------------------------------------------------------#
    # The requester need be a superuser 
    #--------------------------------------------------------------#
    def test_func(self):

        return self.validate()

    def post(self, request, *args, **kwargs):
        """
        Purpose: Add new entity to database
        """

        #Extract params from body
        if request.body is None or request.body is b'':
            return JsonResponse(data={'message':'Post body can not be empty'})
        
        request_data = json.loads(request.body)

        #Ensure required params exist
        entityName = request_data.get('entityName', '')
        industryName = request_data.get('industryName', '')
        
        ##Ensure required params exist
        if entityName == '' or industryName == '':
            return JsonResponse(data={'message':'Error with inputs'})
        
        #Default Non-Education industryId
        industryId = 10000
        currentMaxIndustryId = 0

        try:                        
            # Find the max non-education industry id from table first
            if industryName.lower() == 'education':
                industryId = Entity.objects.filter(Q(industry_name = 'Education')).latest('industry_id').industry_id + 1
            else:
                industryId = Entity.objects.filter(~Q(industry_name = 'Education')).latest('industry_id').industry_id + 1
        except Entity.DoesNotExist:
            pass
      
        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            if not com.checkSuperUser( user_id = self.user.id ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #----------------------------------------------------# 
            # validate the input of entityName
            if not checkStringHasOnlyAlphaAndSpace( entityName ):
                return JsonResponse(data={'message':'Entity name only allows alphabet and space'})

            # validate the input of industryName
            if not checkStringHasOnlyAlphaAndSpace( industryName ):
                return JsonResponse(data={'message':'Industry name only allows alphabet and space'})            
            #----------------------------------------------------# 

            #Initialize tree
            output={
                'entity': {}
            }
            
            #Add entity to table
            newEntity = Entity(
                entity_name=entityName,
                industry_id=industryId,
                industry_name=industryName,
                is_active = True
            )
            newEntity.save()

            #Search groups for given entity id
            output['entity'] = model_to_dict(newEntity)
            return JsonResponse( output )

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def patch(self, request, *args, **kwargs):
        """
        Purpose: Change entity details
        """

        #Extract params from body
        if request.body is None or request.body is b'':
            return JsonResponse(data={'message':'Post body can not be empty'})
        
        request_data = json.loads(request.body)

        entityName = request_data.get('entityName', '')
        industryName = request_data.get('industryName', '')
        entityId = request_data.get('entityId', 0)

        ##Ensure required params exist
        if entityName == '' or industryName == '' or entityId == 0:
            return JsonResponse(data={'message':'Error with inputs'})

        #Modify entity detail
        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            if not com.checkSuperUser( user_id = self.user.id ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #----------------------------------------------------# 
            # validate the input of entityName
            if not checkStringHasOnlyAlphaAndSpace( entityName ):
                return JsonResponse(data={'message':'Entity name only allows alphabet and space'})

            # validate the input of industryName
            if not checkStringHasOnlyAlphaAndSpace( industryName ):
                return JsonResponse(data={'message':'Industry name only allows alphabet and space'})            
            #----------------------------------------------------# 

            #Initialize tree
            output={
                'entity': {}
            }

            #Update entity detail
            updatedEntity = Entity.objects.get(id=entityId)
            updatedEntity.entity_name = entityName
            updatedEntity.industry_name = industryName
            updatedEntity.save()

            #Query database and return result
            output['entity'] = model_to_dict(updatedEntity)
            return JsonResponse(output)

        except Entity.DoesNotExist:
            return JsonResponse(data={'message':"Entity does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def delete(self, request, *args, **kwargs):
        """
        Purpose: Mark entity as in-active
        """

        #Extract params from body
        if request.body is None or request.body is b'':
            return JsonResponse(data={'message':'Post body can not be empty'})
        
        request_data = json.loads(request.body)
        entityId = request_data.get('entityId', 0)

        ##Ensure required params exist
        if entityId == 0:
            return JsonResponse(data={'message':'Error with inputs'})

        #Modify entity detail
        try:
            com = common()
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            if not com.checkSuperUser( user_id = self.user.id ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #Initialize tree
            output={
                'entity': {}
            }

            #Update entity detail
            updatedEntity = Entity.objects.get(id=entityId)
            updatedEntity.is_active = 0
            updatedEntity.date_disabled = timezone.now()
            updatedEntity.save()

            #Query database and return result
            output['entity'] = model_to_dict(updatedEntity)
            return JsonResponse(output)

        except Entity.DoesNotExist:
            return JsonResponse(data={'message':"Entity does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

class reports(validate_request, UserPassesTestMixin, TemplateView):
    #--------------------------------------------------------------#
    # The requester need be a superuser 
    #--------------------------------------------------------------#

    def test_func(self):

        return self.validate()

    def post(self, request, *args, **kwargs):
        """
        Purpose: Add new report to database
        """

        #Extract params from body
        if request.body is None or request.body is b'':
            return JsonResponse(data={'message':'Post body can not be empty'})
        
        request_data = json.loads(request.body)

        #Ensure required params exist
        name = request_data.get('name', '')
        workspaceId = request_data.get('workspaceId', '')
        reportId = request_data.get('reportId', '')
        entityId = request_data.get('entityId', 0)
        permissionId = request_data.get('permissionId', 0)
        categoryId = request_data.get('categoryId', 0)


        ##Ensure required params exist
        if name == '' or workspaceId == '' or reportId == '' or entityId == 0 or permissionId == 0 or categoryId == 0:
            return JsonResponse(data={'message':'Error with inputs'})

        newCodeName = uuid.uuid4()
        while Report.objects.filter(codename=newCodeName).exists():
            newCodeName = uuid.uuid4()

        try:

            com = common()            
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            if not com.checkSuperUser( user_id = self.user.id ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #----------------------------------------------------#
            #input validation
            #----------------------------------------------------#
            if not checkStringHasOnlyAlphaNumberDashAndSpace(name): 
                return JsonResponse(data={'message':'Report name only allows alphabet and space'})

            if not checkStringHasOnlyAlphaNumberDashAndSpace(workspaceId): 
                return JsonResponse(data={'message':'Workspace Id only allows alphabet and space'})

            if not checkStringHasOnlyAlphaNumberDashAndSpace(reportId): 
                return JsonResponse(data={'message':'Report Id only allows alphabet and space'})

            #Initialize tree
            output={
                'report': {}
            }
            
            #Add report to table
            newReport = Report.objects.select_related('permission').select_related('category').create(name=name, codename=newCodeName, workspace_id=workspaceId, report_id=reportId, entity_id=entityId, permission_id=permissionId, category_id=categoryId)

            #Populate report back
            output['report'] = com.toReportDict(newReport)
            return JsonResponse( output )

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def patch(self, request, *args, **kwargs):
        """
        Purpose: Update report details
        """

        #Extract params from body
        if request.body is None or request.body is b'':
            return JsonResponse(data={'message':'Post body can not be empty'})
        
        request_data = json.loads(request.body)

        name = request_data.get('name', '')
        workspaceId = request_data.get('workspaceId', '')
        reportId = request_data.get('reportId', '')
        entityId = request_data.get('entityId', 0)
        permissionId = request_data.get('permissionId', 0)
        categoryId = request_data.get('categoryId', 0)
        isActive = request_data.get('isActive', None)
        pk = request_data.get('id', 0)

        #Ensure required params exist
        if pk == 0 or name == '' or workspaceId == '' or reportId == '' or entityId == 0 or permissionId == 0 or categoryId == 0:
            return JsonResponse(data={'message':'Error with inputs'})

        #Modify report detail
        try:
            com = common()

            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            if not com.checkSuperUser( user_id = self.user.id ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #----------------------------------------------------#
            #input validation
            #----------------------------------------------------#
            if not checkStringHasOnlyAlphaNumberDashAndSpace(name): 
                return JsonResponse(data={'message':'Report name only allows alphabet, numbers, space and dash'})

            if not checkStringHasOnlyAlphaNumberDashAndSpace(workspaceId): 
                return JsonResponse(data={'message':'Workspace Id only allows Report name only allows alphabet, numbers, space and dash'})

            if not checkStringHasOnlyAlphaNumberDashAndSpace(reportId): 
                return JsonResponse(data={'message':'Report Id only allows Report name only allows alphabet, numbers, space and dash'})

            #Initialize tree
            output={
                'report': {}
            }

            #Update report detail
            if isActive is None:
                Report.objects.filter(pk=pk).update(name=name, workspace_id=workspaceId, report_id=reportId, entity_id=entityId, permission_id=permissionId, category_id=categoryId)
            else:
                Report.objects.filter(pk=pk).update(name=name, workspace_id=workspaceId, report_id=reportId, entity_id=entityId, permission_id=permissionId, category_id=categoryId, is_active=isActive)
            updatedReport = Report.objects.select_related('permission').select_related('category').get(id=pk)

            #return report
            output['report'] = com.toReportDict(updatedReport)
            return JsonResponse(output)

        except Report.DoesNotExist:
            return JsonResponse(data={'message':"Report does not exist"})

        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})

    def delete(self, request, *args, **kwargs):
        """
        Purpose: Mark report as in-active
        """

        #Extract params from body
        if request.body is None or request.body is b'':
            return JsonResponse(data={'message':'Post body can not be empty'})
        
        request_data = json.loads(request.body)
        pk = request_data.get('id', 0)

        ##Ensure required params exist
        if pk == 0:
            return JsonResponse(data={'message':'Error with inputs'})

        #Mark report in-active
        try:
            com = common()
            
            #----------------------------------------------------# 
            # check permission starts
            #----------------------------------------------------# 
            if not com.checkSuperUser( user_id = self.user.id ):
                return JsonResponse(data={'message':"No permission"})
            #----------------------------------------------------# 
            # check permission ends
            #----------------------------------------------------# 

            #Initialize tree
            output={
                'report': {}
            }

            #Update entity detail
            updatedReport = Report.objects.get(id=pk)
            updatedReport.is_active = 0
            updatedReport.save()

            #Return report
            output['report'] = model_to_dict(updatedReport)
            return JsonResponse(output)

        except Report.DoesNotExist:
            return JsonResponse(data={'message':"Report does not exist"})
            
        except Exception as e: 
            return JsonResponse(data={'message':repr(e)})