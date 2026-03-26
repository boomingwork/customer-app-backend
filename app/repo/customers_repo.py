from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.db.models import Customer


class CustomerRepository:

    def __init__(self, db: Session):
        self.db = db

    # Check if a customer exists by email OR phone
    def get_by_email_or_phone(self, email: str, phone: str) -> Customer | None:
        stmt = select(Customer).where(
            or_(Customer.email == email, Customer.phone == phone)
        )
        return self.db.scalar(stmt) 

    # Save a new customer
    def save(self, customer: Customer) -> Customer:
        self.db.add(customer)
        return customer

    # Get all customers
    def get_all(self) -> list[Customer]:
        stmt = select(Customer)
        return self.db.scalars(stmt).all()  # scalars() gives list of entities