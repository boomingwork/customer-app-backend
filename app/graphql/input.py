import strawberry

@strawberry.input
class CustomerInput:
    name: str
    email: str
    phone: str