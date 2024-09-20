from flask import Flask, request, jsonify
from flask_cors import CORS
from db.schemas.employees import Employees
from db.schemas.organsiations import Orgs
from utils.data_Normalization import NormalizeData
import json

app = Flask(__name__)
CORS(app)


@app.route("/emplogin", methods=["POST"])
def login():
    data = request.get_data()
    data = data.decode("utf-8")
    login_data = json.loads(data)
    
    try:
        employee = Employees.get((Employees.employee_name == login_data["email"]) & (Employees.password == login_data["password"]))
        return {"Validity": True, "User": employee}
    except Exception as e:
        return {"Validity": False} 
    

@app.route("/CreateEmployee", methods=["POST"])
def CreateEmployee():
    data = request.get_data()
    data = data.decode("utf-8")
    New_Employee_Data = json.loads(data)

    try:
        employee = Employees.get(Employees.employee_name == New_Employee_Data["employee_email"])
        return jsonify({"message": "patient/@exists"})
    except DoesNotExist:
        Employees.insert_many([New_Employee_Data]).execute()
        return jsonify({"message": "patient/@created"})
    except Exception as e:
        print(f"The Error is {e}")
        return jsonify({"message": "error/unexpected"})
    

from peewee import DoesNotExist

@app.route("/CreateOrg", methods=["POST"])
def Create_Organisation():
    data = NormalizeData(request.get_data())
    
    try:
        # Try to find an organization with the given email
        Orgs.get(Orgs.organisation_email == data["organisation_email"])
        # If we reach this point, the organization exists
        return jsonify({"message": "organisation/@exists"})
    except DoesNotExist:
        # If we get here, the organization doesn't exist, so we can create it
        Orgs.create(**data)
        return jsonify({"message": "organisation/@created"})
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An error occurred: {e}")
        return jsonify({"message": "error/@unexpected"}), 500

@app.route("/getOrgsEmps", methods=["POST"])
def get_Organisation_employees():
	data = NormalizeData(request.get_data())
	
	org = Orgs.get(Orgs.organisation_id == data["org_id"])
 
	org_emp = org.onboarding_employees.dicts()
	
	print(org_emp)
	return jsonify(list(org_emp)), 200
    

if __name__ == "__main__":
    app.run(debug=True)