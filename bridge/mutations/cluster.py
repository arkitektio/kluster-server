from koherent.types import Info
from bridge import types, models, inputs, gateway
from bridge.gateway import get_gateway



async def create_dask_cluster(info: Info, input: inputs.CreateClusterInput) -> types.DaskCluster:

    gateway = get_gateway()

    print(input.name)


    new_cluster = await gateway.new_cluster()
    

    return types.DaskCluster(value=new_cluster)