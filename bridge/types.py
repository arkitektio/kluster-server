import strawberry
import strawberry.django
from strawberry import auto
from typing import Optional, cast
import strawberry_django
from bridge import scalars, enums
from django.contrib.auth import get_user_model
import datetime

from dask_gateway.client import ClusterReport
from authentikate.strawberry.permissions import NeedsScopes
from django.conf import settings


@strawberry_django.type(get_user_model(), description="A user of the bridge server. Maps to an authentikate user")
class User:
    """ A user of the bridge server"""
    id: auto
    sub: str
    username: str
    email: str
    password: str


@strawberry.type(description=" A security object for a dask cluster")
class Security:
    """ A security object for a dask cluster. Is used to connect to the dask cluster securely"""
    tls_key: str
    tls_cert: str


GATEWAY_START_STRING = (
    f"gateway://{settings.DASK_GATEWAY_HOST}:{settings.DASK_GATEWAY_PORT}"
)
DASHBOARD_START_STRING = (
    f"http://{settings.DASK_GATEWAY_HOST}:{settings.DASK_GATEWAY_PORT}"
)


@strawberry.type(description=" A dask cluster")
class DaskCluster:
    """ A dask cluster"""
    value: strawberry.Private[ClusterReport]

    @strawberry.field(description="The name of the dask cluster")
    def name(self) -> str:
        """The name of the dask cluster"""
        return cast(str, self.value.name)

    @strawberry.field(description="The id of the dask cluster")
    def id(self) -> strawberry.ID:
        """The id of the dask cluster"""
        return cast(strawberry.ID, self.value.name)

    @strawberry.field(description="A link to the dashboard for the dask cluster. Relative to the proxy.")
    def dashboard_link(self) -> str:
        """ The dashboard link for the dask cluster
        
        Will be a relative link to the proxy, not an absolute link
        to facilitate easy proxying
        """
        return cast(str, self.value.dashboard_link.replace(DASHBOARD_START_STRING, ""))

    @strawberry.field(description="A link to the scheduler for the dask cluster. Relative to the proxy.")
    def scheduler_address(self) -> str:
        """ The scheduler address for the dask cluster

        Will be a relative link to the proxy, not an absolute link
        to facilitate easy proxying
        """
        return cast(str, self.value.scheduler_address.replace(GATEWAY_START_STRING, ""))

    @strawberry.field(description="When the dask cluster was created")
    def start_time(self) -> Optional[datetime.datetime]:
        """ When the dask cluster was created"""
        return cast(datetime.datetime, self.value.start_time)

    @strawberry.field(description="When the dask cluster was stopped")
    def stop_time(self) -> Optional[datetime.datetime]:
        """ When the dask cluster was stopped"""
        return cast(Optional[datetime.datetime], self.value.stop_time)

    @strawberry.field(description="The status of the dask cluster")
    def status(self) -> enums.DaskClusterState:
        """ The status of the dask cluster"""
        if isinstance(self.value.status, str):
            return enums.DaskClusterState(enums.map_string_to_enum(self.value.status))

        return enums.DaskClusterState(self.value.status)

    @strawberry.field(description="The options used to create the dask cluster")
    def options(self) -> scalars.UntypedOptions:
        """ The options used to create the dask cluster"""
        return self.value.options

    @strawberry.field(description="The tags for the dask cluster (currently fake)")
    def tags(self) -> list[str]:
        """ The tags for the dask cluster"""
        return ["fake"]

    @strawberry.field(permission_classes=[NeedsScopes("openid")], description="The user who created the dask cluster")
    def security(self) -> Optional[Security]:
        """ The security object for the dask cluster"""
        if self.value.security is None:
            return None
        return Security(
            tls_key=self.value.security.tls_key, tls_cert=self.value.security.tls_cert
        )
    
    @strawberry.field(description="The user who created the dask cluster")
    def n_workers(self) -> int:
        """ The number of workers in the dask cluster"""
        


        return self.value.n_workers
