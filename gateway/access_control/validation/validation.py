import access_control.validation._jwt_validation as jwt_validation

import urllib
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.http import JsonResponse



Data_Template = { "Data": {}, "Errors": []  }

class validate_request():

    raise_exception = True 
    permission_denied_message = Data_Template # any error message will be written to Errors

    def handle_no_permission(self):
        return JsonResponse(self.permission_denied_message, safe=False, status=401)

    def add_error_message(self, code, message):
        self.permission_denied_message['Errors'] = [ { "Code":code, "Message":message } ]

    def check_user_oid(self,params):
        """
        #First, try to get user from oid
        try:
            #Try getting user
            print('oid:',params['oid'])
            self.user = User.objects.get(oid = params['oid'])

        #If user does not exist, try to match user from email
        except User.DoesNotExist:
            #Perform checks
            if len(params['emails'])==0: raise KeyError()

            #Try getting user
            try:
                #Try getting user
                print('emails:',params['emails'][0])
                self.user = User.objects.get(username = params['emails'][0])

                #Add details to DB
                self.user.oid = params['oid']
                self.user.given_name = params['given_name']
                self.user.family_name = params['family_name']
                self.user.save(update_fields=['oid','given_name','family_name'])

            except User.DoesNotExist:
                raise NameError()

        else:
            return
        """
        return 

    def validate(self):
        #print('in access_control/validation/validate_request/validate()')

        #Check if some type of token parameter exists
        query_parameters = urllib.parse.parse_qs(self.request.META['QUERY_STRING'])#.items()
        #print(('access_token' in query_parameters))
        
        if ( not 'HTTP_AUTHORIZATION' in self.request.META ) & ( not 'access_token' in query_parameters ):
            self.add_error_message('NO_TOKEN' ,'No authorization token is given')
            return False

        else: 
            #Obtain token  
            access_token = None
            if 'access_token' in query_parameters:
                
                access_token = query_parameters['access_token'][0] 
                access_token = access_token.strip()
                #print('access_token = '+access_token)

            if 'HTTP_AUTHORIZATION' in self.request.META: 
                # Option1 -  Authorization : jwt lkjfdsjfsdlkfjdslkfjldsf
                # Option2 -  Authorization : lkjfdsjfsdlkfjdslkfjldsf
                access_token = self.request.META['HTTP_AUTHORIZATION'].strip()
                if ' ' in access_token: access_token = access_token.split(' ')[-1]

            #Validate token    
            try:
                validated_token = jwt_validation.validate_jwt(access_token, settings.TENANT_NAME, settings.POLICY_NAME, settings.APP_ID)

                #Ensure user is in our database and then capture oid
                #self.check_user_oid(validated_token)
                #print(self.user)

            except KeyError as ex:
                print('Error with token keys!')
                self.add_error_message('INVALID_TOKEN' ,'The user-supplied token has key errors.')
                return False

            except NameError as ex:
                print('Error with token and database!')
                self.add_error_message('INVALID_TOKEN' ,'The details in user-supplied token does not match our database records.')
                return False

            except Exception as ex:
                print('The JWT is not valid!')
                self.add_error_message('INVALID_TOKEN' ,'The given authorization token is invalid')
                return False

            else:
                print('The JWT is valid!')
                return True

def validateEntityForUser(user,entity_id):
    """
    #Get user
    groups = User.objects.get(username = user.username).groups.all()

    #Get entity list
    entity_list = list(set(Entity.objects.get(id = g.entity_id).industry_id for g in groups))

    return entity_id in entity_list
    """ 
    return 

