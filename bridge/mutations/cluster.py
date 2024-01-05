from koherent.types import Info
from bridge import types, inputs
from bridge.gateway import get_gateway
import strawberry


async def create_dask_cluster(
    info: Info, input: inputs.CreateClusterInput
) -> types.DaskCluster:
    """ Create a new dask cluster on a bridge server"""
    gateway = get_gateway()

    print(input.name)

    new_cluster = await gateway.new_cluster()

    return types.DaskCluster(value=new_cluster)


async def stop_dask_cluster(info: Info, id: strawberry.ID) -> strawberry.ID:
    """ Stop a dask cluster"""
    gateway = get_gateway()
    await gateway.stop_cluster(id)
    return id
