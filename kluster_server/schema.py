import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry import ID
from kante.directives import upper, replace, relation
from bridge import types
from bridge import mutations
from bridge import queries
import strawberry_django
from koherent.strawberry.extension import KoherentExtension
from bridge.gateway import DaskGatewayExtension


@strawberry.type
class Query:
    """The root query type"""

    dask_clusters: list[types.DaskCluster] = strawberry.field(
        resolver=queries.dask_clusters, description="Return all dask clusters"
    )
    dask_cluster: types.DaskCluster = strawberry.field(
        resolver=queries.dask_cluster, description="Return a dask cluster by id"
    )
    me: types.User = strawberry.field(
        resolver=queries.me, description="Return the currently logged in user"
    )


@strawberry.type
class Mutation:
    """The root mutation type"""

    create_dask_cluster: types.DaskCluster = strawberry_django.mutation(
        resolver=mutations.create_dask_cluster,
        description="Create a new dask cluster on a bridge server",
    )
    stop_dask_cluster: ID = strawberry_django.mutation(
        resolver=mutations.stop_dask_cluster, description="Stop a dask cluster"
    )
    scale_dask_cluster: types.DaskCluster = strawberry_django.mutation(
        resolver=mutations.scale_dask_cluster, description="Scale a dask cluster"
    )


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    directives=[upper, replace, relation],
    extensions=[DjangoOptimizerExtension, KoherentExtension, DaskGatewayExtension],
)
