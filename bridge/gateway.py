from dask_gateway import Gateway
from dask_gateway.auth import GatewayAuth
from django.conf import settings
from contextvars import ContextVar
from strawberry.extensions import SchemaExtension
from kante.types import ChannelsWSContext
from typing import Any

current_dask_gateway: ContextVar[Gateway] = ContextVar("current_dask_gateway")


class JWTAuth(GatewayAuth): # type: ignore
    """Attaches HTTP Bearert Authentication to the given Request object."""

    def __init__(self, token: str) -> None:
        """ Create a new JWTAuth object"""
        self.token = token

        print(self.token)

    def pre_request(self, resp: Any) -> tuple[dict[str, str], None]:
        """ Add the Authorization header to the request
        
        Hook called before the request is made. This hook adds the Authorization
        header to the request."""
        headers = {"Authorization": "Bearer " + self.token}
        return headers, None


def get_gateway() -> Gateway:
    """Get the current Dask Gateway connection

    This function gets the current Dask Gateway connection from the context
    of the GraphQL request. If no Dask Gateway connection is found, an
    exception is raised.

    Returns
    -------
    Gateway
        The Dask Gateway connection

    Raises
    ------
    Exception
        If no Dask Gateway connection is found

    """
    try:
        return current_dask_gateway.get()
    except LookupError:
        raise Exception("No Dask Gateway connection found")


def create_gateway(context: ChannelsWSContext) -> Gateway:
    """Create a new Dask Gateway connection

    Parameters
    ----------
    context : ChannelsWSContext
        The context of the GraphQL request

    Returns
    -------
    Gateway
        The Dask Gateway connection

    """
    gateway = Gateway(
        address=f"http://{settings.DASK_GATEWAY_HOST}:{settings.DASK_GATEWAY_PORT}",
        auth=JWTAuth(context.request.auth.token.raw),
        asynchronous=True,
    )
    return gateway


class DaskGatewayExtension(SchemaExtension):
    """A Strawberry Schema Extension for Dask Gateway"""
    async def on_operation(self) -> None:  # type: ignore
        """Create a new Dask Gateway connection and add it to the context.
        
        Hook is called before the operation is executed. This hook creates a new
        Dask Gateway connection and adds it to the context of the GraphQL request.
        """
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
