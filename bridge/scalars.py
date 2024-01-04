from typing import NewType

import strawberry

UntypedOptions = strawberry.scalar(
    NewType("ArrayLike", object),
    description="The `ArrayLike` scalar type represents a reference to a store "
    "previously created by the user n a datalayer",
    serialize=lambda v: v,
    parse_value=lambda v: v,
)




