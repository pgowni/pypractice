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


class CorporatePolicy(Policy):

    def __init__(self, id, type, start_date, end_date, premium, limit):
        super().__init__(id, type, start_date, end_date, premium)
        self.limit = limit

    #override
    def to_dict(self):
        parent_dict = super().to_dict()
        parent_dict['Limit'] = self.limit
        return parent_dict
