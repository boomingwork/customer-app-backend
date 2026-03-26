import strawberry
from strawberry.types import Info
from typing import List
from sqlalchemy.orm import Session
from app.graphql.type import CustomerType
from app.services.customer_serv import CustomerService

@strawberry.type
class Query:

    @strawberry.field
    def customers(self, info: Info) -> List[CustomerType]:
        db: Session = info.context["db"]
        service = CustomerService(db)
        customers = service.list_customers()
        return [CustomerType(id=c.id, name=c.name, phone=c.phone, email=c.email, created_at=c.created_at) for c in customers]