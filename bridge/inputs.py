from pydantic import BaseModel
from strawberry.experimental import pydantic
import strawberry

class CreateClusterInputModel(BaseModel):
    """Create a dask cluster input model"""
    name: str


@pydantic.input(CreateClusterInputModel, description="Create a dask cluster input")
class CreateClusterInput:
    """Create a dask cluster input"""
    name: str


class ScaleClusterInputModel(BaseModel):
    """Create a dask cluster input model"""
    id: str
    n_workers: int


@pydantic.input(ScaleClusterInputModel, description="Create a dask cluster input")
class ScaleClusterInput:
    """Create a dask cluster input"""
    id: strawberry.ID
    n_workers: int