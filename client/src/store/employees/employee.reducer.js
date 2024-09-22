import { employeesActionTypes } from "./employee.actionTypes";

const Inital_State = {
  employees: [],
};

export const EmployeeReducer = (state = Inital_State, action) => {
  const { type, payload } = action;
  if (type == employeesActionTypes.UPDATE_EMPLOYEES) {
    return {
      ...state,
      employees: payload,
    };
  }
  return state;
};
