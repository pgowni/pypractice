from models import Customer, Policy

class IndividualCustomer(Customer):
    def to_dict(self):
        return super().to_dict()
    

class IndividualPolicy(Policy):
    def to_dict(self):
        return super().to_dict()


