import { employeesActionTypes } from "./employee.actionTypes";

export const updateEmployee = (employees) => {
  return {
    type: employeesActionTypes.UPDATE_EMPLOYEES,
    payload: employees,
  };
};
