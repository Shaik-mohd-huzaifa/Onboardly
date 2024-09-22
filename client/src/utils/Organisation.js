import axios from "axios";

export const CreateOrganisation = async (OrgInfo) => {
  try {
    const res = await axios.post("http://127.0.0.1:5000/CreateOrg", OrgInfo);
    console.log(res.data);
    return res.data;
  } catch (error) {
    return error;
  }
};
