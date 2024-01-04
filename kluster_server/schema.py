from kante.types import Info
from typing import AsyncGenerator
import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension
from bridge.channel import cluster_listen
from strawberry import ID
from kante.directives import upper, replace, relation
from strawberry.permission import BasePermission
from typing import Any, Type
from bridge import types, models
from bridge import mutations
from bridge import queries
from strawberry.field_extensions import InputMutationExtension
import strawberry_django
from koherent.strawberry.extension import KoherentExtension
from bridge.gateway import DaskGatewayExtension
from authentikate.strawberry.permissions import HasScopes, IsAuthenticated, NeedsScopes




@strawberry.type
class Query:
    dask_clusters = strawberry.field(resolver=queries.dask_clusters)
    dask_cluster = strawberry.field(resolver=queries.dask_cluster)
    me: types.User = strawberry.field(resolver=queries.me)
    


@strawberry.type
class Mutation:
    create_dask_cluster: types.DaskCluster = strawberry_django.mutation(
        resolver=mutations.create_dask_cluster,
    )
    
    


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    directives=[upper, replace, relation],
    extensions=[
        DjangoOptimizerExtension,
        KoherentExtension,
        DaskGatewayExtension
    ],
)
