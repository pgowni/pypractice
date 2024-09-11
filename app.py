from flask import Flask, request, jsonify
import json
from models import Customer, Policy
from corporate import CorporateCustomer, CorporatePolicy
from individual import IndividualCustomer, IndividualPolicy

app = Flask(__name__)

def help_load_customers(list):
    customer_objects = []

    for customer in list:
        if customer["CustomerType"] == "Corporate":
            new_obj = CorporateCustomer.to_obj(customer)
            customer_objects.append(new_obj) 
        
        else:
            new_obj = IndividualCustomer.to_obj(customer)
            customer_objects.append(new_obj) 
    
    return customer_objects

def load_customers():
    try:
        with open("data\customers.json", 'r') as input_file:
            customers_list = json.load(input_file)
    except FileNotFoundError as fe:
        return("File does not exist")
    else: 
        return help_load_customers(customers_list)

def write_customers(data):
    customer_data = []
    
    for customer_obj in data:
            customer_data.append(customer_obj.to_dict())
    
    try:
        with open("data\customers.json", 'w') as output_file:
            json.dump(customer_data, output_file, indent=4) 
    except FileNotFoundError as fe:
        return("File does not exist")
    except:
        return("Other error")
    else:
        pass


@app.route("/")
def home_page():
    all_customer_obj = load_customers()
    all_customers = []

    for customer_obj in all_customer_obj:
        all_customers.append(customer_obj.to_dict())

    return jsonify(all_customers)

@app.route("/add_customer",methods=['POST'])
def add_customer():
    new_customer = request.get_json()
    all_customers = load_customers()
    curr_policy_id = Policy.generate_policy_id()
    new_policy_id = "POL" + str(int(curr_policy_id[3:]) + 1)
   
    for person in all_customers:
        if (person.to_dict()["FirstName"]+ person.to_dict()["LastName"])  == (new_customer["FirstName"]+ new_customer["LastName"]):
            new_policy_id = curr_policy_id
            return "Cannot add an existing customer. Try updating their existing information instead"
   
    new_customer["policies"].append(new_policy_id)
    try:
        if new_customer["CustomerType"] == "Corporate":
            all_customers.append(CorporateCustomer.to_obj(new_customer))
        
        else:
            all_customers.append(IndividualCustomer.to_obj(new_customer))
        
        write_customers(all_customers)
    except Exception as e:
        new_policy_id = curr_policy_id
        print("Error is that", e.args)
        return "Failed to add customer"
    else:
        return "Successfully added customer"

@app.route("/delete_customer",methods=['DELETE'])
def delete_customer():
    all_customers = load_customers()
    customer_to_remove = request.get_json()

    for person in all_customers:
        if person["Email"] == customer_to_remove["Email"]:
            all_customers.remove(person)
            write_customers(all_customers)
            return "Succesfully deleted customer"        
    return "Customer doesn't exist in system"
    
@app.route("/update_customer",methods=['PUT', 'PATCH'])
def update_customer():
    all_customers = load_customers()
    customer_to_update = request.get_json()
    attributes_to_update = customer_to_update.keys()

    for person in all_customers:
        if person["CustomerID"] == customer_to_update["CustomerID"]:
            for attribute in attributes_to_update:
                person[attribute] = customer_to_update[attribute]
            write_customers(all_customers)
            return "Succesfully updated customer"
    
    return "Customer doesn't exist in system"


def help_load_policies(list):

    policy_objects = []
    for policy in list:
        if policy["PolicyType"] == "Individual":
            new_obj = IndividualPolicy.to_obj(policy)
            policy_objects.append(new_obj)
        
        else:
            new_obj = CorporatePolicy.to_obj(policy)
            policy_objects.append(new_obj)
    
    return policy_objects


def load_policies():
    try:
        with open("data\policies.json", 'r') as input_file:
            policies_list = json.load(input_file)
    except FileNotFoundError as fe:
        return("File does not exist")
    else:
        return help_load_policies(policies_list)

def write_policies(data):
    policy_data = []
    
    for obj in data:
        policy_data.append(obj.to_dict())
    
    try:
        with open("data\policies.json", 'w') as output_file:
            json.dump(policy_data, output_file, indent=4) 
    except FileNotFoundError as fe:
        return("File does not exist")
    except:
        return("Other error")
    else:
        pass

@app.route("/policies")
def view_policies():
    all_policy_obj = load_policies()
    all_policies = []
    
    for policy_obj in all_policy_obj:
        all_policies.append(policy_obj.to_dict())    
    return jsonify(all_policies) 

@app.route("/add_policy", methods=["POST"])
def add_policy():
    
    all_policies = load_policies()
    curr_policy_id = Policy.generate_policy_id()
    new_policy = request.get_json()
    new_policy_id = "POL" + str(int(curr_policy_id[3:]) + 1)
    
    if not new_policy["PolicyID"]:
        new_policy["PolicyID"] = new_policy_id

    # Check if a customer with this policy ID exists
    # customer_found = None
    # for customer in all_customers:
    #     if customer["PolicyID"] == new_policy["PolicyID"]:
    #         customer_found = customer
    #         break

    # if not customer_found:
    #     return "Cannot add policy: No customer associated with this Policy ID"
    
    if new_policy["PolicyType"] == "Individual":
         all_policies.append(IndividualPolicy.to_obj(new_policy))
    
    else:
        all_policies.append(CorporatePolicy.to_obj(new_policy))
    
    try:
        write_policies(all_policies)
    except:
        return("Could not add policy")
    else:
        return ("Successfully added policy")
        

if __name__ == '__main__':
    app.run(debug=True)
