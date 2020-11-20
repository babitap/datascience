
import graphene
import api.graphqlapi.schema_acara 

# quick test on graphQL
class Category( graphene.ObjectType ):
    category  = graphene.String()
    description = graphene.String()
    token   = graphene.String()

class AllCategories( graphene.ObjectType ):
    all_categories = graphene.List(Category)

    def resolve_all_categories(self, info, **kwargs):
        # some logic to validate the jwt 

        auth_header = info.context.META.get('HTTP_AUTHORIZATION')

        temp = []
        temp.append( Category( category = 'C1', description='hello', token=auth_header ) )
        temp.append( Category( category = 'C2', description='world', token=auth_header ) )
        temp.append( Category( category = 'C3', description='fred', token=auth_header ) )

        return temp

# now add all available datasets in the list 
class Query( api.graphqlapi.schema_acara.AcaraSchoolMasters, 
            #AllCategories,  
            graphene.ObjectType):
    print('I am in Query()')
    pass


schema = graphene.Schema(query=Query)