from bridge.gateway import get_gateway
from bridge import types, filters
from strawberry_django import pagination
import strawberry
from typing import List


async def dask_clusters(
    filters: filters.ClusterFilter | None = None,
    pagination: pagination.OffsetPaginationInput | None = None,
) -> List[types.DaskCluster]:
    """ Return all dask clusters"""
    clusters = await get_gateway().list_clusters()

    if filters:
        print(clusters)
        if filters.ids:
            clusters = [x for x in clusters if x.name in filters.ids]

        if filters.search:
            print(filters.search)
            clusters = [x for x in clusters if str(x.name).startswith(filters.search)]

    print(clusters)

    return [types.DaskCluster(value=y) for y in clusters]


async def dask_cluster(id: strawberry.ID) -> types.DaskCluster:
    """ Return a dask cluster by id"""
    x = await get_gateway().get_cluster(id)
    return types.DaskCluster(value=x)
