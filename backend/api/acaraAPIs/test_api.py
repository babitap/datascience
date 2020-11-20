from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from access_control.validation.validation import validate_request

from access_control.validation.decorators import custom_permission_required
from access_control.models import *
from access_control.dbviews.classbasedviews import *
from access_control.dbviews.helpers import *

import pandas as pd

class test_url(validate_request, UserPassesTestMixin, TemplateView):

    def test_func(self):
        return self.validate()

    #@custom_permission_required("add_group")
    def get(self, request, **kwargs):

        print('HIIIIIII')
        industry_name='Education'

        #Add 5 users
        if(0):
            User.objects.create_user(username = 'user1@email.com')
            User.objects.create_user(username = 'user2@email.com')
            User.objects.create_user(username = 'user3@email.com', created_by_id=2)
            User.objects.create_superuser(username = 'superuser@email.com')
            User.objects.create_findexuser(username = 'findexuser@email.com')
            User.objects.create_findexuser_all(username = 'findexuser_all@email.com')

        if(0):
            #Get acara entities
            acara_file=os.path.join('access_control','data','school-profile-2008-2018.xlsx')
            df_excel=pd.read_excel(acara_file,sheet_name='School Profile',usecols=['ACARA SML ID','School Name'],index_col=False)
            entities=df_excel.drop_duplicates().values
            for entity in entities:
                Entity(
                    entity_name=entity[1],
                    industry_id=entity[0],
                    industry_name=industry_name,
                    is_active=True
                ).save()

        if(0):
            #Add permissions from file
            perm_file=os.path.join('access_control','data','permissions.csv')
            df_perms=pd.read_csv(perm_file,index_col=False)
            for i,row in df_perms.iterrows():
                Permission(
                    name=row['name'],
                    codename=row['codename'],
                    is_findex=row['is_findex'],
                    is_findex_all=row['is_findex_all'],
                    is_accessible=row['is_accessible']
                ).save()


        #Add 10 schools
        entities=[
            [40000,'Corpus Christi Catholic School'],
            [40001,'Fahan School'],
            [40002,'Geneva Christian College'],
            [40003,'Holy Rosary Catholic School'],
            [40004,'Immaculate Heart of Mary Catholic School'],
            [40005,'John Calvin School'],
            [40006,'Larmenier Catholic School'],
            [40007,'Launceston Church Grammar School'],
            [40008,'St James Catholic College'],
            [40009,'Our Lady of Lourdes Catholic School'],
            [40010,'Our Lady of Mercy Catholic School']
        ]
        #Add 3 groups to schools
        groups=[
        'Principal & Admin', 
        'Teachers', 
        'Other Staff'
        ]
        if(0):
            for entity in entities:
                entity_id = getattr(Entity.objects.get(industry_id=entity[0], industry_name=industry_name), 'id')
                print(entity_id)

                for group in groups:
                    EntityGroup(
                        name=group,
                        description='NEW GROUP',
                        entity_id=entity_id
                    ).save()



        if(0):
            #Add users to groups
            users=['user1@email.com','user2@email.com']
            for user in users:

                #Select user & group
                my_user = User.objects.get(username = user)
                my_group = EntityGroup.objects.get(name='Other Staff', entity_id=5)

                #Add to group
                my_user.groups.add(my_group)


                #Add permissions to group
                perms=['add_group','change_group','delete_group','view_group']
                for perm in perms:

                    #Select perm
                    my_perm = Permission.objects.get(codename=perm)

                    #Add perm
                    my_group.permissions.add(my_perm)

        if(1):
            #Check perms
            my_user = User.objects.get(username = 'findexuser@email.com')
            print(my_user)
            print(my_user.get_all_permissions())
            print('>>',my_user.has_perm('delete_group'))

            my_perm = Permission.objects.get(codename='add_group')
            print(my_perm.is_findex)


        response={'FUNC RUN':True}

        return JsonResponse(response)