import strawberry
from strawberry.types import Info
from app.graphql.type import CustomerType
from app.graphql.input import CustomerInput
from app.services.customer_serv import CustomerService

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_customer(self, info: Info, input: CustomerInput) -> CustomerType:
        db = info.context["db"]
        service = CustomerService(db)
        try:
            customer = service.create_customer(name=input.name, email=input.email, phone=input.phone)
            return CustomerType(id=customer.id, name=customer.name, phone=customer.phone, email=customer.email, created_at=customer.created_at)
        except ValueError as e:
            raise Exception(str(e))