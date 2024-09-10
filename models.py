class Customer:
    def __init__(self, id, type, first_name, last_name, email, dob, policies):
        self.id = id
        self.type = type
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.dob = dob
        self.policies = policies

    def to_dict(self):
        return {

            "CustomerID": self.id,
            "CustomerType": self.type,
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "Email": self.email,
            "DateOfBirth": self.dob,
            "policies": self.policies
        }
    

class Policy:
    def __init__(self, id, type, start_date, end_date, premium):
        self.id = id
        self.type = type
        self.start_date = start_date
        self.end_date = end_date
        self.premium = premium

    def to_dict(self):
        return {
            "PolicyID": self.id,
            "PolicyType": self.type,
            "StartDate": self.start_date,
            "EndDate": self.end_date,
            "Premium": self.premium
        }

    # @staticmethod
    # def generate_policy_id(policies):
    #     dict_policies = []

    #     for obj in policies:
    #         dict_policies.append(obj.to_dict())
        
    #     if not dict_policies:
    #         return "POL10001"  
        
    #     last_policy_id = 0
    #     for policy in dict_policies:
    #         last_policy_id = max(last_policy_id, int(policy["PolicyID"][3:]))
    #     new_policy_id = f"POL{last_policy_id + 1}"
    #     return new_policy_id

