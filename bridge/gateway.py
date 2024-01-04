from dask_gateway import Gateway, BasicAuth
from .models import OmeroUser
from contextlib import contextmanager
from django.conf import settings
from contextvars import ContextVar
from strawberry.extensions import SchemaExtension
from asgiref.sync import sync_to_async
from typing import Optional
from kante.types import ChannelsWSContext
current_dask_gateway: ContextVar[Gateway] = ContextVar("current_dask_gateway")
from dask_gateway.auth import GatewayAuth


class JWTAuth(GatewayAuth):
    """Attaches HTTP Basic Authentication to the given Request object."""

    def __init__(self, token):
        self.token = token

        print(self.token)

    def pre_request(self, resp):
        headers = {"Authorization": "Bearer " + self.token}
        return headers, None


@sync_to_async
def get_omero_user(context: ChannelsWSContext) -> Optional[OmeroUser]:
    if not context.request.user.is_authenticated:
        raise Exception("User is not authenticated")

    user = OmeroUser.objects.filter(user=context.request.user).first()
    return user


def get_gateway() -> Gateway:
    try:
        return current_dask_gateway.get()
    except LookupError:
        raise Exception("No Dask Gateway connection found")
    


def create_gateway(context: ChannelsWSContext) -> Gateway:
    gateway = Gateway(
        address=f"http://{settings.DASK_GATEWAY_HOST}:{settings.DASK_GATEWAY_PORT}",
        auth=JWTAuth(context.request.auth.token.raw),
        asynchronous=True,
    )
    return gateway



class DaskGatewayExtension(SchemaExtension):

    async def on_operation(self): # type: ignore
        print("Starting operation")
        try:
            
            gateway = create_gateway(self.execution_context.context)
            token = current_dask_gateway.set(gateway)

            try:
                yield
            finally:
                current_dask_gateway.reset(token)
                await gateway.close()
        except Exception as e:
            print(e)
            yield
