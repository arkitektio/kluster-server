from django.db.models import TextChoices
import strawberry
from enum import Enum



@strawberry.enum
class DaskClusterState(int, Enum):
    PENDING = 1
    RUNNING = 2
    STOPPING = 3
    STOPPED = 4
    FAILED = 5



def map_string_to_enum(string):
    return DaskClusterState[string.upper()]