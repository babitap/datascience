import access_control.validation._jwt_validation as jwt_validation

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.http import JsonResponse


Data_Template = { "Data": {}, "Errors": []  }

# Class TemplateView_B2C
#   how to use: 
class TemplateView_B2C(UserPassesTestMixin, TemplateView):

    # If raise_exception attribute is set to True, a PermissionDenied exception is raised when the conditions are not met.
    #  When False (the default), anonymous users are redirected to the login page.
    raise_exception = True 
    permission_denied_message   =  Data_Template # any error message will be written to Errors

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

                #Add oid to DB
                self.user.oid = params['oid']
                self.user.save(update_fields=['oid'])

            except User.DoesNotExist:
                raise NameError()

        else:
            return
        """

        return 

    def test_func(self):

        #print(self.request.META)
        if not 'HTTP_AUTHORIZATION' in self.request.META:
            self.add_error_message('NO_TOKEN' ,'No authorization token is given')
            return False 
        else: 
            access_token = self.request.META['HTTP_AUTHORIZATION']
            access_token = access_token.strip()
            # Option1 -  Authorization : jwt lkjfdsjfsdlkfjdslkfjldsf
            # Option2 -  Authorization : lkjfdsjfsdlkfjdslkfjldsf
            if ' ' in access_token: access_token = access_token.split(' ')[-1]
            validated_token = None

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
                self.request.user.username = validated_token['emails'][0]
                print('The JWT is valid!')
                return True

    # Please rewrite get() function to return the dataset. 