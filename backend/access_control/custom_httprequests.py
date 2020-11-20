from django.http import QueryDict
from django.http import HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
import json 

class HttpPostTunnelingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        '''
        param_dict = {}
        #Modify file if patch or delet
        if request.method in ["POST","PATCH","DELETE"] and request.content_type == "application/json":
            # request.POST is empty 
            # we only have request.body which is raw string 
            print('HttpPostTunnelingMiddleware process_request()')
            param_dict = json.loads( request.body ) 
            request.POST = QueryDict(param_dict, mutable=True)
        '''    
            
        if request.method in ["PATCH","DELETE", "POST"] and request.content_type != "application/json":
            method=request.method
            if hasattr(request, '_post'):
                del request._post
                del request._files
            try:
                request.method = "POST"
                request._load_post_and_files()
                request.method = method
            except AttributeError as e:
                request.META['REQUEST_METHOD'] = 'POST'
                request._load_post_and_files()
                request.META['REQUEST_METHOD'] = method
            #Create new request entry
            if method=='PATCH': request.PATCH = request.POST
            elif method=='DELETE': request.DELETE = request.POST
