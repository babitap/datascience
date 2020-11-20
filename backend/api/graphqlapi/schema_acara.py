
from api.graphqlapi.shema_shared import *
from api.graphqlapi.schema_acara_dashboard import *
from api.graphqlapi.schema_acara_benchmark import *

class AcaraUserSchoolQuery( graphene.ObjectType ): 
    selectedSchool = graphene.Field( AcaraSchoolMasterType, userId = graphene.Int()  )

    def resolve_selectedSchool(self, info, userId=None, **kwargs): 
        user = info.context.user
        default_entity = user.get_default_school()
        q_filter = Q_list()
        q_filter.add_Q( Q(acara_id=default_entity.acara_id) ) # at this moment, we hardcode to St Anne
        return AcaraSchoolMaster.objects.using(DEFAULT_ACARA_DATABASE).get(  q_filter.get_filter()  )


class AcaraQuery( graphene.ObjectType ): 
    

    acaraDashboardQuery = graphene.Field( AcaraDashboardQuery )

    acaraBenchmarkQuery = graphene.Field( AcaraBenchmarkQuery )

    """
    acaraUserSelectedSchoolQuery = graphene.Field( AcaraUserSchoolQuery )

    acaraSchoolMasters = graphene.List( AcaraSchoolMasterType,  \
                                            id = graphene.Int(), \
                                            nameSearch = graphene.String(), \
                                            idIn=graphene.List(graphene.Int, description="ID List") ) 
    """

    def resolve_acaraDashboardQuery(self, info, **kwargs):
        return AcaraDashboardQuery()
    
    def resolve_acaraBenchmarkQuery(self, info, **kwargs):
        return AcaraBenchmarkQuery()    

    """
    def resolve_acaraSchoolMasters(self, info,  id=None, nameSearch=None, idIn=None,**kwargs):

        # The value sent with the search parameter will be in the args variable
        Q_list = []
        filter = None

        if id: 
            Q_list.append( Q(acara_id=id) )

        if nameSearch: 
            Q_list.append( Q(school_name__contains=nameSearch)) 

        if idIn:
            Q_list.append( Q(acara_id__in=idIn)) 

        if len(Q_list) > 0:
            for i in range(0, len(Q_list) ): 
                if i == 0: 
                    filter = Q_list[0]
                else: 
                    filter = filter & Q_list[i]

        #To only return entities that user associated with if user doesn't have view_all_schools permission
        user = info.context.user
        if(user.has_perm('view_all_schools') is False):
            entity_list = user.get_entity_industryIds()
            if(filter is None):
                filter = Q(acara_id__in=entity_list)
            else:
                filter = filter & Q(acara_id__in=entity_list)         

            return AcaraSchoolMaster.objects.using(DEFAULT_ACARA_DATABASE).filter( filter )
        else: 
            return AcaraSchoolMaster.objects.using(DEFAULT_ACARA_DATABASE).all()
    

    def resolve_acaraUserSelectedSchoolQuery(self, info, **kwargs):
        return AcaraUserSchoolQuery()
    
    """