import strawberry_django
from bridge import models
from typing import List, Optional
from strawberry import ID
import strawberry
from pydantic import BaseModel
from strawberry.experimental import pydantic


class CreateClusterInputModel(BaseModel):
    name: str


@pydantic.input(CreateClusterInputModel)
class CreateClusterInput:
    name: str



