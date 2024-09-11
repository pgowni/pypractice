import json

class Customer:
    def __init__(self, id, type, first_name, last_name, email, dob, policies):
        self.id = id
        self.type = type
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.dob = dob
        self.policies = policies
    
    @staticmethod
    def to_obj(data):
        return Customer(
            id = data['CustomerID'],
            type = data['CustomerType'],
            first_name = data['FirstName'],
            last_name = data['LastName'],
            email = data['Email'],
            dob = data['DateOfBirth'],
            policies = [policy for policy in data["policies"]]
        )

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
    
    def total_premium(self):
        total = 0
        with open("JSON\policies.json", 'r') as input_file:
            curr_customer_policies = json.load(input_file) 
        for policy in curr_customer_policies:
            if policy["PolicyID"] in set(self.policies):
                total += policy["Premium"]
        
        return total


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
    
    @staticmethod
    def to_obj(data):
        return Policy(
            id=data['PolicyID'],
            type=data['PolicyType'],
            start_date=data['StartDate'],
            end_date=data['EndDate'],
            premium=data['Premium'],
        )
    # @classmethod
    # def generate_policy_id():
    #     print("Before", cls.curr_policy_id)
    #     id_serial = int(cls.curr_policy_id[3:])
    #     id_serial += 1
    #     cls.curr_policy_id = cls.curr_policy_id[:3] + str(id_serial)
    #     print("After", cls.curr_policy_id)
    #     return cls.curr_policy_id

    @staticmethod
    def generate_policy_id():
        print
        try:
            with open("data\policies.json", 'r') as input_file:
                policies_list = json.load(input_file)
        except FileNotFoundError as fe:
            return("File does not exist")
        
        print(policies_list)
        latest_id = 0
        for policy in policies_list:
            latest_id = max(latest_id, int(policy["PolicyID"][3:]))


        return "POL"+str(latest_id)

    

