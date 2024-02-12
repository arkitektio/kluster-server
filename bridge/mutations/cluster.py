from koherent.types import Info
from bridge import types, inputs
from bridge.gateway import get_gateway
import strawberry
from dask_gateway import Options


async def create_dask_cluster(
    info: Info, input: inputs.CreateClusterInput
) -> types.DaskCluster:
    """ Create a new dask cluster on a bridge server"""
    gateway = get_gateway()

    options = await gateway.cluster_options() 

    print("MY OPTION", options)

    new_cluster = await gateway.new_cluster(cluster_options=None)

    return types.DaskCluster(value=new_cluster)


async def scale_dask_cluster(
    info: Info, input: inputs.ScaleClusterInput
) -> types.DaskCluster:
    """ Scale a dask cluster"""
    gateway = get_gateway()
    await gateway.scale_cluster(input.id, input.n_workers)


    value = await gateway.get_cluster(input.id)
    return types.DaskCluster(value=value)




async def stop_dask_cluster(info: Info, id: strawberry.ID) -> strawberry.ID:
    """ Stop a dask cluster"""
    gateway = get_gateway()
    await gateway.stop_cluster(id)
    return id
