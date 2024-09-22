import { GetEmployees } from "../../utils/GetEmployees";
import { useDispatch, useSelector } from "react-redux";
import { EmployeeSelector } from "../../store/employees/employee.selector";
import { updateEmployee } from "../../store/employees/employee.actions";
import { useEffect, useState } from "react";
import { organisationSelector } from "../../store/Organisation/organisation.selector";
import { Oval } from "react-loader-spinner";
import axios from "axios";
import "./EmployeePath.Styles.scss";

export const EmployeePage = () => {
  const dispatch = useDispatch();
  const Empdata = useSelector(EmployeeSelector);
  const Org = useSelector(organisationSelector);
  const [employees, setEmployees] = useState(Empdata);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newEmployee, setNewEmployee] = useState({
    employee_name: "",
    employee_email: "",
    password: "",
    employee_type: "",
    organisation_id: Org.organisation_id,
    onboarding: true,
  });

  useEffect(() => {
    async function getEmployees() {
      setLoading(true);
      const data = await GetEmployees(Org.organisation_id);
      dispatch(updateEmployee(data));
      setLoading(false);
      setEmployees(data);
    }

    getEmployees();
  }, [dispatch]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewEmployee({ ...newEmployee, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/CreateEmployee",
        newEmployee,
      );
      if (response.status === 200) {
        setIsModalOpen(false);
        const updatedEmployees = await GetEmployees("30001");
        dispatch(updateEmployee(updatedEmployees));
        setEmployees(updatedEmployees);
      }
    } catch (error) {
      console.error("Error adding employee:", error);
    }
  };

  return (
    <div className="employee-page">
      <h1 className="employee-title">Employee Page</h1>
      <button
        className="add-employee-button"
        onClick={() => setIsModalOpen(true)}
      >
        Add Employee
      </button>
      {loading ? (
        <Oval width="30px" height="30px" color="blue" />
      ) : (
        <div className="employee-list">
          {employees &&
            employees.map((employee) => (
              <div key={employee.employee_email} className="employee-item">
                <p className="employee-email">{employee.employee_email}</p>
                <p className="employee-name">{employee.employee_name}</p>
                <p className="employee-type">{employee.employee_type}</p>
              </div>
            ))}
        </div>
      )}

      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <h2>Add New Employee</h2>
            <form onSubmit={handleSubmit} className="employee-form">
              <input
                type="text"
                name="employee_name"
                value={newEmployee.employee_name}
                onChange={handleInputChange}
                placeholder="Employee Name"
                required
              />
              <input
                type="email"
                name="employee_email"
                value={newEmployee.employee_email}
                onChange={handleInputChange}
                placeholder="Employee Email"
                required
              />
              <input
                type="password"
                name="password"
                value={newEmployee.password}
                onChange={handleInputChange}
                placeholder="Password"
                required
              />
              <input
                type="text"
                name="employee_type"
                value={newEmployee.employee_type}
                onChange={handleInputChange}
                placeholder="Employee Type"
                required
              />
              <select
                name="onboarding"
                value={newEmployee.onboarding}
                onChange={handleInputChange}
                required
              >
                <option value={true}>Yes</option>
                <option value={false}>No</option>
              </select>
              <button type="submit" className="submit-button">
                Add Employee
              </button>
            </form>
            <button
              className="close-button"
              onClick={() => setIsModalOpen(false)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
