from graphene_django.views import GraphQLView

import access_control.validation._jwt_validation as jwt_validation
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
import urllib.parse, re

Data_Template = { "Data": {}, "Errors": []  }

class TokenAuthGraphQLView(GraphQLView):
    graphiql = True
    # as_view() is an in-built function in GraphQLView, we hardcode it here to enable graphiql 
    #def as_view(self, enable_graphiql=True ):  
    #    return super.as_view(graphiql=True)

    def add_error_message(self, code, message):
        error_context = Data_Template
        error_context['Errors'] = [ { "Code":code, "Message":message } ]
        return error_context

    def parseQueryParams(self, s):
        d = {}
        for k,v in urllib.parse.parse_qs(s).items():
            #print("{} = {}".format(k,v))
            d[k] = v
        return d


    def dispatch(self, request, *args, **kwargs):
        flag = False
        
        query_parameters = self.parseQueryParams( self.request.META['QUERY_STRING'] ) 

        if ( not 'HTTP_AUTHORIZATION' in self.request.META ) & ( not 'access_token' in query_parameters )  : 
            error_json = self.add_error_message('NO_TOKEN' ,'No authorization token is given')
            return JsonResponse(error_json, safe=False, status=401)
        else: 
            access_token = None
            if 'access_token' in query_parameters:
                access_token = query_parameters['access_token'][0] 
                access_token = access_token.strip()

            if 'HTTP_AUTHORIZATION' in self.request.META: 
                # Option1 -  Authorization : jwt lkjfdsjfsdlkfjdslkfjldsf
                # Option2 -  Authorization : lkjfdsjfsdlkfjdslkfjldsf
                access_token = self.request.META['HTTP_AUTHORIZATION'].strip()
                access_token = access_token.split(' ')[-1]

            #Validate token    
            try:
                validated_token = jwt_validation.validate_jwt(access_token, settings.TENANT_NAME, settings.POLICY_NAME, settings.APP_ID)
            except Exception as ex:
                print('The JWT is not valid!')
                #self.add_error_message('INVALID_TOKEN' ,'The given authorization token is invalid')
                flag = False
            else:
                print('The JWT is valid!')
                flag = True


            if flag:
                return super().dispatch(request, *args, **kwargs)
            else:
                #error_message = Data_Template
                #error_message['Errors'] = [ {"Code" :'INVALID_TOKEN', "Message":'The given authorization token is invalid' } ] 
                error_json = self.add_error_message('INVALID_TOKEN' ,'The given authorization token is invalid')
                return JsonResponse(error_json, safe=False, status=401)