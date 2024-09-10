from models import Customer, Policy

class CorporateCustomer(Customer):

    def __init__(self, id, type, first_name, last_name, email, dob, company, policies):
        super().__init__(id, type, first_name, last_name, email, dob, policies)
        self.company = company
    
    #override
    def to_dict(self):
        parent_dict = super().to_dict()
        parent_dict['Company'] = self.company
        return parent_dict
    
    #override
    @staticmethod
    def to_obj(data):
        customer_object = Customer.to_obj(data)
        return CorporateCustomer(
            id = customer_object.id,
            type = customer_object.type,
            first_name = customer_object.first_name,
            last_name = customer_object.last_name,
            email = customer_object.email,
            dob = customer_object.dob,
            policies = customer_object.policies,
            company = data['Company']
        )
    

class CorporatePolicy(Policy):

    def __init__(self, id, type, start_date, end_date, premium, limit):
        super().__init__(id, type, start_date, end_date, premium)
        self.limit = limit

    #override
    def to_dict(self):
        parent_dict = super().to_dict()
        parent_dict['Limit'] = self.limit
        return parent_dict
    
    #override
    @staticmethod
    def to_obj(data):
        policy_object = Policy.to_obj(data)
        return CorporatePolicy(
            id = policy_object.id,
            type = policy_object.type,
            start_date = policy_object.start_date,
            end_date = policy_object.end_date,
            premium = policy_object.premium,
            limit = data['Limit']
        )
