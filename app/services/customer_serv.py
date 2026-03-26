from sqlalchemy.orm import Session
from app.db.models import Customer
from app.repo.customers_repo import CustomerRepository


class CustomerService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = CustomerRepository(db)

    # Create customer with validation
    def create_customer(self, name: str, email: str, phone: str) -> Customer:

        existing_customer = self.repo.get_by_email_or_phone(email, phone)

        if existing_customer:
            if existing_customer.email == email:
                raise ValueError("A customer with this email already exists")
            if existing_customer.phone == phone:
                raise ValueError("A customer with this phone already exists")

        new_customer = Customer(name=name, email=email, phone=phone)
        self.repo.save(new_customer)

        # Commit + refresh
        self.db.commit()
        self.db.refresh(new_customer)
        return new_customer

    # List all customers
    def list_customers(self) -> list[Customer]:
        return self.repo.get_all()