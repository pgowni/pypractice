from models import Customer, Policy

class IndividualCustomer(Customer):
    def to_dict(self):
        return super().to_dict()
    
    @staticmethod
    def to_obj(data):
        return Customer.to_obj(data)
    

class IndividualPolicy(Policy):
    def to_dict(self):
        return super().to_dict()
    
    @staticmethod
    def to_obj(data):
       return Policy.to_obj(data)
    


