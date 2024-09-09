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
            print("here", customer)
            new_obj = CorporateCustomer(
            customer["CustomerID"], 
            customer["CustomerType"],
            customer["FirstName"], 
            customer["LastName"], 
            customer["Email"], 
            customer["DateOfBirth"],
            customer["Company"], 
            [policy['policyID'] for policy in customer["policies"]]
            )
            customer_objects.append(new_obj) 
        
        else:
            new_obj = IndividualCustomer(
            customer["CustomerID"], 
            customer["CustomerType"],
            customer["FirstName"], 
            customer["LastName"], 
            customer["Email"], 
            customer["DateOfBirth"],
            [policy['policyID'] for policy in customer["policies"]]
            )
            customer_objects.append(new_obj) 
    
    return customer_objects

def load_customers():
    try:
        with open("JSON\customers.json", 'r') as input_file:
            customers_list = json.load(input_file)
    except FileNotFoundError as fe:
        return("File does not exist")
    else: 
        return help_load_customers(customers_list)

def write_customers(data):
    try:
        with open("JSON\customers.json", 'w') as output_file:
            json.dump(data, output_file, indent=4) 
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
    all_customers = load_customers()
    new_customer = request.get_json()
    all_policies = load_policies()
    
    for person in all_customers:
        if (person["FirstName"]+ person["LastName"])  == (new_customer["FirstName"]+ new_customer["LastName"]):
            return "Cannot add an existing customer. Try updating their existing information instead"
        
    all_customers.append(new_customer)
    write_customers(all_customers)
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
            new_obj = IndividualPolicy(
            policy["PolicyID"], 
            policy["PolicyType"], 
            policy["StartDate"], 
            policy["EndDate"], 
            policy["Premium"], 
            )
            policy_objects.append(new_obj)
        
        else:
            new_obj = CorporatePolicy(
            policy["PolicyID"], 
            policy["PolicyType"], 
            policy["StartDate"], 
            policy["EndDate"], 
            policy["Premium"],
            policy["Limit"] 
            )
            policy_objects.append(new_obj)
    
    return policy_objects


def load_policies():
    try:
        with open("JSON\policies.json", 'r') as input_file:
            policies_list = json.load(input_file)
    except FileNotFoundError as fe:
        return("File does not exist")
    else:
        return help_load_policies(policies_list)

def write_policies(data):
    try:
        with open("JSON\policies.json", 'w') as output_file:
            json.dump(data, output_file, indent=4) 
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


if __name__ == '__main__':
    app.run(debug=True)
