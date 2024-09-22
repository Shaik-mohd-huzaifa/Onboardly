import { orgActionTypes } from "./organisation.actionTypes";

const Inital_State = {
  org_info: {},
};

export const OrganisationReducer = (state = Inital_State, action) => {
  const { type, payload } = action;

  if (type == orgActionTypes.UPDATE_ORG) {
    return {
      ...state,
      org_info: payload,
    };
  }

  return state;
};
