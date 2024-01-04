import strawberry
import strawberry.django
from strawberry import auto
from typing import List, Optional, Annotated, Union, cast, Any
import strawberry_django
from bridge import models, scalars, filters, enums
from django.contrib.auth import get_user_model
from koherent.models import AppHistoryModel
from authentikate.strawberry.types import App
from kante.types import Info
import datetime

from itertools import chain
from enum import Enum
from strawberry.experimental import pydantic
from pydantic import BaseModel
from dask_gateway.client import ClusterReport
from authentikate.strawberry.permissions import HasScopes, IsAuthenticated, NeedsScopes
from django.conf import settings

@strawberry_django.type(get_user_model())
class User:
    id: auto
    sub: str
    username: str
    email: str
    password: str


@strawberry.type(description=" A security object for a dask cluster")
class Security:
    tls_key: str 
    tls_cert: str


GATEWAY_START_STRING = f"gateway://{settings.DASK_GATEWAY_HOST}:{settings.DASK_GATEWAY_PORT}"
DASHBOARD_START_STRING = f"http://{setttings.DASK_GATEWAY_HOST}:{settings.DASK_GATEWAY_PORT}"



@strawberry.type(description=" A dask cluster")
class DaskCluster:
    value: strawberry.Private[ClusterReport]

    @strawberry.field
    def name(self) -> str:
        return cast(str, self.value.name)
    
    @strawberry.field
    def id(self) -> strawberry.ID:
        return cast(strawberry.ID, self.value.name)
    

    @strawberry.field
    def dashboard_link(self) -> str:
        return cast(str,self.value.dashboard_link.replace(DASHBOARD_START_STRING, ""))
    
    @strawberry.field
    def scheduler_address(self) -> str:
        return cast(str,self.value.scheduler_address.replace(GATEWAY_START_STRING, ""))
    
    @strawberry.field
    def start_time(self) -> Optional[datetime.datetime]:
        return self.value.start_time
    
    @strawberry.field
    def stop_time(self) -> Optional[datetime.datetime]:
        return self.value.stop_time
    
    @strawberry.field
    def status (self) -> enums.DaskClusterState:
        if isinstance(self.value.status, str):
            return enums.DaskClusterState(enums.map_string_to_enum(self.value.status))

        return enums.DaskClusterState(self.value.status)
    

    @strawberry.field
    def options(self) -> scalars.UntypedOptions:
        return self.value.options

    
    @strawberry.field
    def tags(self) -> list[str]:
        return ["fake"]
    
    @strawberry.field(permission_classes=[NeedsScopes("openid")])
    def security(self) -> Optional[Security]:
        if self.value.security is None:
            return None
        return Security(tls_key=self.value.security.tls_key, tls_cert=self.value.security.tls_cert)






