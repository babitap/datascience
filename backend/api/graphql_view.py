from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.db import connections

from access_control.validation.decorators import custom_permission_required
from access_control.validation.validation import validate_request
from graphene_django.views import GraphQLView

class graphql_view(validate_request, GraphQLView):

    #@custom_permission_required("add_group")
    def dispatch(self, request, *args, **kwargs):

        if self.validate():
            if(request.user.id is None):
                request.user = self.user
            print(request.POST)
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()
