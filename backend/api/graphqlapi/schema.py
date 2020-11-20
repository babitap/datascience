
import graphene
from api.graphqlapi.schema_acara import AcaraQuery

class Query( AcaraQuery ,  graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)