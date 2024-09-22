import { combineReducers } from "redux";
import { EmployeeReducer } from "./employees/employee.reducer";
import { OrganisationReducer } from "./Organisation/organisation.reducer";

export const rootReducer = combineReducers({
  employees: EmployeeReducer,
  organisation: OrganisationReducer,
});
