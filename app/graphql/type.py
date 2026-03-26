import strawberry
from datetime import datetime

@strawberry.type
class CustomerType:
    id: int
    name: str
    phone: str
    email: str
    created_at: datetime