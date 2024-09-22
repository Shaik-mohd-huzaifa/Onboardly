import { orgActionTypes } from "./organisation.actionTypes";

export const updateOrg = (org_info) => {
  return {
    type: orgActionTypes.UPDATE_ORG,
    payload: org_info,
  };
};
