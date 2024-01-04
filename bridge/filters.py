import strawberry
from bridge import models
from koherent.strawberry.filters import ProvenanceFilter
from strawberry import auto
from typing import Optional, Any
from strawberry_django.filters import FilterLookup
from django.db.models import QuerySet, Model
from kante.types import Info








@strawberry.input
class ClusterFilter():
    ids: list[strawberry.ID] | None = None
    search: str | None = None
    pass

