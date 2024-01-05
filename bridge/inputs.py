from pydantic import BaseModel
from strawberry.experimental import pydantic


class CreateClusterInputModel(BaseModel):
    """Create a dask cluster input model"""
    name: str


@pydantic.input(CreateClusterInputModel, description="Create a dask cluster input")
class CreateClusterInput:
    """Create a dask cluster input"""
    name: str
